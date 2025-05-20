import threading


class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Logger, cls).__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.logs = []

    def log(self, message):
        self.logs.append(message)
        print(f"[LOG]: {message}")

    def get_logs(self):
        return self.logs
