class Package:
    def __init__(self, name: str, launch: str, leader=False):
        self.package_name = name
        self.launch_file = launch
        self.leader = leader

    def getRunCommand(self):
        return f"ros2 launch {self.package_name} {self.launch_file}"
    
    def isLeader(self):
        return self.leader
    
    def __str__(self) -> str:
        return f"{self.package_name} package with launch file {self.launch_file} is a leader : {self.leader}"