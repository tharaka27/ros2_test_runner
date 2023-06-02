from package import Package 

class Testcase:
    def __init__(self, name: str, numberOfInvocations: int, checkpoint: str, terminate: str, askToTerminate:str, pre_commands:list, packages : Package):
        self.name = name
        self.numberOfInvocations = numberOfInvocations
        self.packages = list(map( lambda package: Package(**package), packages )) #for package in packages 
        self.checkpoint = checkpoint
        self.terminate = terminate
        self.askToTerminate = askToTerminate
        self.pre_commands = pre_commands

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
    
    def __str__(self) -> str:
        return f"{self.name} testcase with {self.numberOfInvocations} number of invocations"