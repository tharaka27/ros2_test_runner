from package import Package
from testcase import Testcase
from packagerunner import PackageRunner
import json
import time
from typing import List
from logger import Logger
import psutil
import threading

def main():

    #with open('config_asynchronous.json', 'r') as file:
    with open('config_synchronous.json', 'r') as file:
    #with open('config_baseline.json', 'r') as file:
        config = json.load(file)

    testcase_list : List[Testcase] = []

    logger = Logger(f"logs/LogFile_{int(time.time())}.txt")

    for testcase in config["testcases"]:
        testcase = Testcase(**testcase)
        testcase_list.append(testcase)
        
    for testcase in testcase_list:
        logger.log("================================================================\n")
        logger.log(f"Starting {str(testcase)}" )
        print(f"Starting {str(testcase)}" )

        runner = PackageRunner(testcase, logger)
        runner.run()
        print(f"Ending {str(testcase)}" )
        time.sleep(5)
        for process in testcase.getKillProcess():
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] == process:
                    print("Process" , process, "is still running pid: ", proc.pid )
                    print("Killing process")
                    proc.kill()


    
    
if __name__ == '__main__':
    main()