from concurrent.futures import ThreadPoolExecutor
import os
import config

class ThreadPool:

    def __init__(self, num_workers = os.cpu_count() + 1) -> None:
        self.num_workers = num_workers
        if config.verbose:
            print(f'Using {self.num_workers} threads in thread pool')
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.current_thread_idx = 0

    def __del__(self):
        self.executor.shutdown()

    def submit_task(self, task, *args):
        self.executor.submit(task, *args)
