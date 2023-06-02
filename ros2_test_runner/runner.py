#from util import Package
from package import Package
from testcase import Testcase
#from util import PackageRunner
import json
import time

def main():

    with open('config copy.json', 'r') as file:
        config = json.load(file)

    package_list = []

    #for package in config["packages"]:
    #    package_list.append(Package(**package))

    #print (json.dumps(config, sort_keys=True, indent=4))

    # runner = PackageRunner(config)

    for testcase in config["testcases"]:
        testcase = Testcase(**testcase)
            
     
    # for package in package_list:
    #     runner.addPackage(package)
    
    # #for i in range(config["numberOfInvocations"]):
    # runner.run()
    # time.sleep(10)
        
    # print("Processes terminated")

if __name__ == '__main__':
    main()