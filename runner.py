from util import Package
from util import PackageRunner

def main():
    
    package_1 = Package("panda_moveit_config", "moveit.launch.py", False)
    
    package_2 = Package("paper_benchmarks", "benchmark_asynchronous.launch.py", True)

    
    runner = PackageRunner()
    runner.addPackage(package=package_1)
    runner.addPackage(package=package_2)

    runner.run()

    print("Processes terminated")

if __name__ == '__main__':
    main()