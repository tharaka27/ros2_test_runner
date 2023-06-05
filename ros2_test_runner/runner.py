from package import Package
from testcase import Testcase
from packagerunner import PackageRunner
import json
import time
from typing import List
from logger import Logger

def main():

    with open('config.json', 'r') as file:
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
    
    
if __name__ == '__main__':
    main()