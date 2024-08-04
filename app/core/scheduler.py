import threading
import time
import schedule
from django.utils import timezone
from concurrent.futures import ThreadPoolExecutor
from .models import Task

class Scheduler:
    pool = None
    stop_scheduler_event = None

    def __init__(self, _workers=None):
        self.pool = ThreadPoolExecutor(_workers or 4)

    def __del__(self):
        self.pool.shutdown()
        self.stop_scheduler_event()

    def query_runnable(self):
        tasks = Task.objects.filter(
            state=Task.State.PENDING
        ).filter(
            available_at__lte=timezone.now()
        )
        return tasks

    def init_schedule_loop(self, interval=1):
        def run_continuously():
            """Continuously run, while executing pending jobs at each
            elapsed time interval.
            @return cease_continuous_run: threading. Event which can
            be set to cease continuous run. Please note that it is
            *intended behavior that run_continuously() does not run
            missed jobs*. For example, if you've registered a job that
            should run every minute and you set a continuous run
            interval of one hour then your job won't be run 60 times
            at each interval but only once.
            """
            stop_scheduler_event = threading.Event()

            class ScheduleThread(threading.Thread):
                @classmethod
                def run(cls):
                    while not stop_scheduler_event.is_set():
                        schedule.run_pending()
                        time.sleep(interval)

            continuous_thread = ScheduleThread()
            continuous_thread.start()
            return stop_scheduler_event

        schedule.every(5).seconds.do(self.task_loop)
        schedule.every(2).minutes.do(self.cleaner_loop)
        self.stop_scheduler_event = run_continuously()
        print("Initiated Scheduler")

    def cleaner_loop(self):
        # Get unreasonably long-running tasks and forcefully error them
        # IMPROVEMENT: This should be best implemented by also checking on the workers
        now = timezone.now()
        tasks = Task.objects.filter(
            state=Task.State.RUNNING
        ).filter(
            updated_at__lte=now - timezone.timedelta(minutes=2)
        ).filter(
            available_at__lte=now
        )

        for task in tasks:
            # IMPROVEMENT: Should be reported, in a real setting
            print(f"[Scheduler] Clean: {task}. Lifespan: {now - task.updated_at}")
            task.state = Task.State.ERRORED
            task.available_at = None
            task.save()

    def task_loop(self):
        tasks = self.query_runnable()

        for task in tasks:
            print(f"[Scheduler] Start: {task}. Input: {task.data_input}")
            self.run_task(task)
            print(f"[Scheduler] End: {task}. Output: {task.data_output}")

        # Testing purpose before populer
        Task.objects.create(
            data_input={ 'a': 5, 'b': 2 }
        )
        Task.objects.create(
            task_type=Task.Task_type.ADD,
            data_input={ 'a': 5, 'b': 2 }
        )
        Task.objects.create(
            task_type=Task.Task_type.DIVIDE,
            data_input={ 'a': 5, 'b': 0 }
        )

    def run_task(self, task):
        task.state = Task.State.RUNNING
        task.save()

        try:
            task.data_output = task.run()
            task.state = Task.State.COMPLETED
            task.available_at = None
        except Exception as e:
            if task.retry > 0:
                task.retry -= 1
                task.state = Task.State.PENDING
                task.available_at = timezone.now() + timezone.timedelta(seconds=10) # Backoff time before retry
            else:
                task.state = Task.State.ERRORED
                task.available_at = None
        finally:
            task.save()
