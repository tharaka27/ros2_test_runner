import subprocess
import time
import signal
import threading
import os

class Package:
    def __init__(self, name: str, launch: str, leader=False):
        self.package_name = name
        self.launch_file = launch
        self.leader = leader

    def getRunCommand(self):
        return f"ros2 launch {self.package_name} {self.launch_file}"
    
    def isLeader(self):
        return self.leader
    
class PackageRunner:
    def __init__(self, config: dict):
        self.name = ""
        self.package_list = []
        self.pre_process_commands = config["pre_commands"] #["cd /home/ros/ws_moveit ", ". install/setup.sh "]
        self.subprocess_list = []
        self.is_leader_dead = False
        self.thread_list = []
        self.lock = threading.Lock()
        self.config = config
    
    def addPackage(self, package: Package):
        self.package_list.append(package)

    def signal_handler(self, sig, frame):
        for process in self.subprocess_list:
            try:
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            except Exception as e:
                print(e)
        exit(0)

    def run(self):
        signal.signal(signal.SIGINT, self.signal_handler)

        numPackages = len(self.package_list)
        for i in range(numPackages):
            thread = threading.Thread(target=self.launch_package, args=(i,))
            thread.start()
            time.sleep(2)
            self.thread_list.append(thread)

        for i in range(numPackages):
            self.thread_list[i].join()

        for process in self.subprocess_list:
            process.wait()
    
    def launch_package(self, number:int):
        package = self.package_list[number]
        self._launch_package(package)
    
    def _launch_package(self, package: Package):
        command = "&& ".join(self.pre_process_commands)
        command = f"{command} && {package.getRunCommand()}" 

        with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, \
                            stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True,\
                                preexec_fn=os.setsid) as process:
            self.subprocess_list.append(process)
            if package.isLeader():
                try:
                    with open("example.txt", 'w') as file:
                        for line in process.stdout:
                            print(line, end='') # process line here
                            if self.config["terminate"] in line:
                                print("Killing Leader")
                                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                                with self.lock:
                                    self.is_leader_dead = True
                            if self.config["checkpoint"] in line:
                                print("checkpoint reached")
                                file.write(line)
                    print("File written successfully.")
                except IOError:
                    print(f"Error writing to file example.txt.")

            else:
                for line in process.stdout:
                    print(line, end='') # process line here
                    with self.lock:
                        if self.is_leader_dead:
                            print("Killing Follower")
                            os.killpg(os.getpgid(process.pid), signal.SIGTERM)