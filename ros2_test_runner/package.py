class Package:
    def __init__(self, name: str, launch: str, ros_args:dict, leader=False):
        self.package_name = name
        self.launch_file = launch
        self.leader = leader
        self.ros_args = ros_args

    def getRunCommand(self):
        string = ""
        for key, value in self.ros_args.items():
            string = key + ":=" + str(value) + " "

        return f"ros2 launch {self.package_name} {self.launch_file} {string}"
    
    def isLeader(self):
        return self.leader
    
    def __str__(self) -> str:
        return f"{self.package_name} package with launch file {self.launch_file} is a leader : {self.leader}"