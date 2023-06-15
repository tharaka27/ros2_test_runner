from package import Package 

class Testcase:
    def __init__(self, name: str, numberOfInvocations: int, checkpoint: str, terminate:\
                  list, askToTerminate: list, pre_commands:list, packages : Package, kill_processes : list):
        self.name = name
        self.numberOfInvocations = numberOfInvocations
        self.packages = list(map( lambda package: Package(**package), packages )) #for package in packages 
        self.checkpoint = checkpoint
        self.terminate = terminate
        self.askToTerminate = askToTerminate
        self.pre_commands = pre_commands
        self.kill_processes = kill_processes

    def getName(self):
        return self.name
    
    def getNumberOfInvocations(self):
        return self.numberOfInvocations
    
    def getPackages(self):
        return self.packages
    
    def getCheckpoint(self):
        return self.checkpoint
    
    def getTerminate(self):
        return self.terminate
    
    def getAskToTerminate(self):
        return self.askToTerminate
    
    def getPrecommands(self):
        return self.pre_commands
    
    def getKillProcess(self):
        return self.kill_processes
    
    def __str__(self) -> str:
        return f"{self.name} with {self.numberOfInvocations} number of invocations"