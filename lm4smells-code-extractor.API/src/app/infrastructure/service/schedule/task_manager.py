from concurrent.futures import ThreadPoolExecutor, Future
import threading

class TaskManager:
    def __init__(self, max_workers=5):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.cancel_flags: dict[str, threading.Event] = {}
        self.tasks: dict[str, Future] = {}

    def schedule(self, task_id: str, use_case, use_case_args):
        cancel_event = threading.Event()
        self.cancel_flags[task_id] = cancel_event

        def task_wrapper():
            use_case(*use_case_args, cancel_event)

        future = self.executor.submit(task_wrapper)
        self.tasks[task_id] = future

    def cancel(self, task_id: str):
        if task_id in self.cancel_flags:
            self.cancel_flags[task_id].set()

    def is_running(self, task_id: str) -> bool:
        future = self.tasks.get(task_id)
        if not future:
            return False
        return not future.done()
