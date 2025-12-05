# utils.py
import time
import sys
import threading

class ASCIILoader:
    def __init__(self, message="Loading"):
        self.message = message
        self.running = False
        self.thread = None
        
    def _animate(self):
        frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        idx = 0
        while self.running:
            sys.stdout.write(f"\r{frames[idx]} {self.message}...")
            sys.stdout.flush()
            idx = (idx + 1) % len(frames)
            time.sleep(0.1)
    
    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._animate)
        self.thread.start()
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 10) + "\r")
        sys.stdout.flush()

def with_loading(message="Processing"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            loader = ASCIILoader(message)
            loader.start()
            try:
                result = func(*args, **kwargs)
                time.sleep(0.5)  # Brief pause for visual effect
                return result
            finally:
                loader.stop()
        return wrapper
    return decorator