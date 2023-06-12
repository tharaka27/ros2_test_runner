from package import Package
from testcase import Testcase
from packagerunner import PackageRunner
import json
import time
from typing import List
from logger import Logger
import threading

def main():

    #with open('config_asynchronous.json', 'r') as file:
    #with open('config_synchronous.json', 'r') as file:
    with open('config_baseline.json', 'r') as file:
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
        time.sleep(10)
    
    
if __name__ == '__main__':
    main()