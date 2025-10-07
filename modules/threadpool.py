from concurrent.futures import ThreadPoolExecutor
import threading
import os
import config

class ThreadPool(ThreadPoolExecutor):

    def thread_factory(self) -> threading.Thread:
        thread = threading.Thread()
        thread.daemon = True
        return thread

    def __init__(self, num_workers) -> None:

        if num_workers == 0:
            num_workers = os.cpu_count() + 1

        super().__init__(max_workers=num_workers)
        self._thread_factory = self.thread_factory

        if config.verbose:
            print(f'Using {num_workers} threads in thread pool')
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.current_thread_idx = 0

    def __del__(self):
        self.shutdown()

    def submit_task(self, task, *args):
        self.submit(task, *args)
