import subprocess
import time
import signal
import threading
import os
import queue
import sys

# class Package:
#     def __init__(self, name: str, launch: str, leader=False):
#         self.package_name = name
#         self.launch_file = launch
#         self.leader = leader

#     def getRunCommand(self):
#         return f"ros2 launch {self.package_name} {self.launch_file}"
    
#     def isLeader(self):
#         return self.leader
    
class PackageRunner:
    def __init__(self, config: dict):
        self.name = ""
        self.package_list = []
        self.pre_process_commands = config["pre_commands"]
        self.subprocess_list = {}
        self.thread_list = []
        self.lock = threading.Lock()
        self.config = config
        self.queue = queue.Queue()
        self.is_shutdown = False
        self.supervisor_thread = None

    def addPackage(self, package: Package):
        self.package_list.append(package)

    def signal_handler(self, sig, frame):
        print("SIGINT raised")
        for pid, process in self.subprocess_list.items():
            try:
                os.killpg(os.getpgid(pid=pid), signal.SIGTERM)
            except Exception as e:
                print(e)
        sys.exit(0)

    def run(self):
        # set signal handler
        signal.signal(signal.SIGINT, self.signal_handler)

        # create threads for each process
        for i in range(len(self.package_list)):
            thread = threading.Thread(target=self._launch_package, args=(i,))
            thread.start()
            time.sleep(3)
            self.thread_list.append(thread)

        # start the execution of the supervisor thread
        self.supervisor_thread = threading.Thread(target=self._launch_supervisor)
        self.supervisor_thread.start()

        # wait till all the threads are joined
        for i in range(len(self.thread_list)):
            self.thread_list[i].join()

        # wait till the supervisor is joined
        self.supervisor_thread.join()

        
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
        package  = self.package_list[number]

        print(f"Starting processing thread {number}")

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
                    with open(self.config["output_file"], 'a') as file:
                        for line in process.stdout:
                            #print(line, end='') # process line here
                            if self.config["terminate"] in line:
                                print("Killing Leader")
                                file.write(line)
                                self.is_shutdown = True
                            if self.config["checkpoint"] in line:
                                print("checkpoint reached")
                                file.write(line)
                    print("File written successfully.")
                except IOError:
                    print(f"Error writing to file example.txt.")

            else:
                for line in process.stdout:
                    if self.config["askToTerminate"] in line:
                        self.is_shutdown = True
                    #print(line, end='') # process line here