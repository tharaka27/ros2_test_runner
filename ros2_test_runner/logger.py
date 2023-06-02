import threading

class Logger:
    def __init__(self, filename):
        self.lock = threading.Lock()
        self.file = open(filename, "a")
    
    def log(self, message):
        with self.lock:
            self.file.write(message + "\n")

    def close(self):
        self.file.close()