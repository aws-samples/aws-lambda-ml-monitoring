import time

class TimerError(Exception):
    """Exception found in Timer class"""
    
class Timer:
    def __init__(self):
        self._start_time = None
        
    def start(self):
        """Starts a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it first")
        
        self._start_time = time.perf_counter()
        
    def stop(self):
        """Stops the timer and returns the time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
            
        total_time = time.perf_counter() - self._start_time
        self._start_time = None
        # print(f"Total time: {total_time*1000:0.4f} milliseconds")
        # Rounding to 4 decimal places, probably good enough
        result = round(total_time*1000,1)
        return(result)