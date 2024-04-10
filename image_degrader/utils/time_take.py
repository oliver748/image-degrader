import time

class TimeTake:
    def __init__(self, debug=False):
        self.start_time = time.perf_counter()
        self.debug = debug
        self.i = 1

    def __enter__(self):
        if self.debug: print(f"\n# # # # DEBUG TRACKING {self.i} # # # #")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        if self.debug: print(f"# # # # TIME: {self.elapsed_time:.2f}s # # # #")
        if self.debug: self.i += 1