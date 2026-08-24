import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class ScheduledTask:
    callback: Callable[..., Any]
    args: tuple = ()
    kwargs: dict = None
    delay: float = 0.0
    interval: float = 0.0
    repeat: bool = False
    
    def __post_init__(self):
        if self.kwargs is None:
            self.kwargs = {}


class Scheduler:
    
    def __init__(self):
        self.queue = []
        self.running = False
        self.thread = None
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run_loop, daemon=True)
            self.thread.start()
            print("[Scheduler] Started")
    
    def stop(self):
        self.running = False
        with self.condition:
            self.condition.notify_all()
        if self.thread:
            self.thread.join(timeout=1.0)
            print("[Scheduler] Stopped")
    
    def schedule(self, callback: Callable[..., Any], delay: float = 0.0, 
                 args: tuple = (), kwargs: dict = None, repeat: bool = False, 
                 interval: float = 0.0) -> ScheduledTask:
        task = ScheduledTask(
            callback=callback,
            args=args,
            kwargs=kwargs or {},
            delay=delay,
            interval=interval,
            repeat=repeat
        )
        
        with self.lock:
            self.queue.append(task)
            self.condition.notify()
        
        return task
    
    def schedule_once(self, callback: Callable[..., Any], delay: float = 0.0,
                      args: tuple = (), kwargs: dict = None) -> ScheduledTask:
        return self.schedule(callback, delay=delay, args=args, 
                           kwargs=kwargs, repeat=False)
    
    def schedule_repeat(self, callback: Callable[..., Any], interval: float,
                        args: tuple = (), kwargs: dict = None) -> ScheduledTask:
        return self.schedule(callback, delay=interval, args=args,
                           kwargs=kwargs, repeat=True, interval=interval)
    
    def cancel(self, task: ScheduledTask):
        with self.lock:
            if task in self.queue:
                self.queue.remove(task)
    
    def _run_loop(self):
        while self.running:
            current_time = time.time()
            tasks_to_run = []
            tasks_to_keep = []
            
            with self.lock:
                for task in self.queue:
                    if task.delay <= current_time:
                        tasks_to_run.append(task)
                        if task.repeat:
                            task.delay = current_time + task.interval
                            tasks_to_keep.append(task)
                    else:
                        tasks_to_keep.append(task)
                
                self.queue = tasks_to_keep
            
            # Run tasks outside the lock to avoid deadlocks
            for task in tasks_to_run:
                try:
                    task.callback(*task.args, **task.kwargs)
                except Exception as e:
                    print(f"[Scheduler] Task failed: {e}")
            
            # Sleep briefly to avoid busy waiting
            with self.condition:
                if self.queue:
                    next_delay = min(task.delay - time.time() for task in self.queue)
                    wait_time = max(0.1, min(next_delay, 1.0))
                    self.condition.wait(wait_time)
                else:
                    self.condition.wait(1.0)