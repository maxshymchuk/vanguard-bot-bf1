from concurrent.futures import ThreadPoolExecutor

class ThreadPool:

    def __init__(self, num_workers) -> None:
        self.num_workers = num_workers
        self.executor = ThreadPoolExecutor(max_workers=num_workers)
        self.current_thread_idx = 0

    def __del__(self):
        self.executor.shutdown()

    def submit_task(self, task, *args):
        self.executor.submit(task, *args)
