import threading

class Logger:
    def __init__(self, filename):
        self.lock = threading.Lock()
        self.file = open(filename, "a")
    
    def log(self, message, ends="\n"):
        with self.lock:
            self.file.write(message + ends)

    def close(self):
        self.file.close()