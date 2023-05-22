class Package:
    def __init_(self, name, launch, leader=False):
        self.package_name = name
        self.launch_file = launch
        self.leader = leader

    def getRunCommand(self):
        return f"ros2 launch {self.package_name} {self.launch_file}"
    
    def isLeader(self):
        return self.leader
    
    