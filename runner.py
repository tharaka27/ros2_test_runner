from util import Package
from util import PackageRunner
import json

def main():

    with open('config.json', 'r') as file:
        config = json.load(file)

    package_list = []

    for package in config["packages"]:
        package_list.append(Package(**package))

    runner = PackageRunner(config)
     
    for package in package_list:
        runner.addPackage(package)
    
    runner.run()
    print("Processes terminated")

if __name__ == '__main__':
    main()