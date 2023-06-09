import subprocess
import time
import signal
import threading
import os
import sys
from package import Package
from testcase import Testcase
from logger import Logger
from typing import List

    
class PackageRunner:
    def __init__(self, testcase : Testcase, logger:Logger):
        self.pre_process_commands = testcase.getPrecommands()
        self.numberOfInvocations = testcase.getNumberOfInvocations()
        self.terminate = testcase.getTerminate()
        self.checkpoint = testcase.getCheckpoint()
        self.askToTerminate = testcase.getAskToTerminate()
        self.subprocess_list = {}
        self.threadList = []
        self.is_shutdown = False
        self.supervisor_thread = None
        self.packageList : List[Package] = []
        self.logger = logger
        for package in testcase.getPackages():
            self.packageList.append(package)
        

    def signal_handler(self, sig, frame):
        print("SIGINT raised")
        for pid, process in self.subprocess_list.items():
            try:
                os.killpg(os.getpgid(pid=pid), signal.SIGTERM)
            except Exception as e:
                print(e)
        self.logger.close()
        sys.exit(0)
        #return False

    def run(self):
        # set signal handler

        for invocation in range(self.numberOfInvocations):
            self.logger.log(f"starting invocation {invocation+1}/{self.numberOfInvocations}")
        
            signal.signal(signal.SIGINT, self.signal_handler)

            # create threads for each process
            for i in range(len(self.packageList)):
                thread = threading.Thread(target=self._launch_package, args=(i,))
                thread.start()
                time.sleep(3)
                self.threadList.append(thread)

            # start the execution of the supervisor thread
            self.supervisor_thread = threading.Thread(target=self._launch_supervisor)
            self.supervisor_thread.start()

            # wait till all the threads are joined
            for i in range(len(self.threadList)):
                self.threadList[i].join()

            # wait till the supervisor is joined
            self.supervisor_thread.join()

            # resetting values to start the new invocation
            self.threadList = []
            self.supervisor_thread = None
            self.is_shutdown = False
            self.subprocess_list = {}

            # give time to close all the proccess
            time.sleep(10)
            

    def _launch_supervisor(self):
        while(True):
            if self.is_shutdown:
                for pid, process in self.subprocess_list.items():
                    try:
                        os.killpg(os.getpgid(pid=pid), signal.SIGTERM)
                    except Exception as e:
                        print(e)
                sys.exit(0)
            else:
                time.sleep(1)
    
    def _launch_package(self, number: int):
        # get the process attached to the thread
        package  = self.packageList[number]

        self.logger.log(f"Starting processing thread {number}")

        time.sleep(1)

        # construct the run command with pre commands
        command = "&& ".join(self.pre_process_commands)
        command = f"{command} && {package.getRunCommand()}" 

        # start the process 
        # only the leader should be allowed to open the file for writing
        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
                            stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True,\
                                preexec_fn=os.setsid) as process:
            self.subprocess_list[process.pid] = process
            if package.isLeader():
                try:
                    for line in process.stdout:
                        print(line, end='') # process line here
                        for terminate_line in self.terminate:
                            if terminate_line in line:
                                print("Killing Leader")
                                self.logger.log(line, ends="")
                                self.is_shutdown = True
                        if self.checkpoint in line:
                            print("checkpoint reached")
                            self.logger.log(line, ends="")
                    print("File written successfully.")
                except IOError:
                    print(f"Error writing to file example.txt.")

            else:
                for line in process.stdout:
                    for terminate_line in self.askToTerminate: 
                        if terminate_line in line:
                            self.is_shutdown = True
                    print(line, end='') # process line here