import subprocess
import threading
import os
import signal
import time

subprocesses = []

pre_process_commands = [
    "cd /home/ros/ws_moveit ",
    "source install/setup.bash "
]

isLeaderDead = False

def launch_package(package_name, launch_file, terminante_string, is_leader):
    cmd = f"ros2 launch {package_name} {launch_file}"
    jointed_commands = "&& ".join(pre_process_commands)
    cmd = "cd /home/ros/ws_moveit && . install/setup.sh && " + cmd 
    command = f"gnome-terminal -- bash -c '{cmd}'"

    global isLeaderDead
    global subprocesses
    
    with subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE, \
                          stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True, preexec_fn=os.setsid) as p:
        subprocesses.append(p)
        if is_leader:
            try:
                with open("example.txt", 'w') as file:
                    for line in p.stdout:
                        print(line, end='') # process line here
                        if "[terminate]" in line:
                            print("Killing Leader")
                            os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                            isLeaderDead = True
                        if "[checkpoint]" in line:
                            print("checkpoint reached")
                            file.write(line)
                print("File written successfully.")
            except IOError:
                print(f"Error writing to file '{file_path}'.")

        else:
            for line in p.stdout:
                print(line, end='') # process line here
                if isLeaderDead:
                    print("Killing Follower")
                    os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                
    
def run_command_1():
    package1_process = launch_package("panda_moveit_config", "moveit.launch.py", "spawing new cube", False)
    # Process or display the stdout and stderr as needed

def run_command_2():
    package2_process = launch_package("paper_benchmarks", "benchmark_asynchronous.launch.py", "spawing new cube", True)


def signal_handler(sig, frame):
    global subprocesses
    for process in subprocesses:
        try:
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except Exception as e:
            print(e)
    exit(0)

file_path = "example.txt"

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)

    thread_1 = threading.Thread(target=run_command_1)
    thread_2 = threading.Thread(target=run_command_2)
    thread_1.start()
    time.sleep(3)
    thread_2.start()

    # Wait for the threads to finish
    thread_1.join()
    thread_2.join()

    for process in subprocesses:
        process.wait()

    print("Processes terminated")