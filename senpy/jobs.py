from datetime import datetime, timezone, timedelta
from time import sleep

from .notifications import notify_me
from .request_utils import post, get, put, handle_request_error
from .cli import print_error
from datetime import datetime
from threading import Timer

def _date_to_str(date):
    return date.strftime("%Y-%m-%dT%H:%M:%SZ")

def _now():
    return datetime.now(tz=timezone.utc)

def _create_job(time_started, total_iteration, current_iteration, job_name):
    body = {
        "time_started_pck": _date_to_str(time_started),
        "total_iteration": total_iteration,
        "current_iteration": current_iteration,
        "job_name": job_name,
    }
    res = post("job/create_job", json=body)
    if 'python_error' not in res and res.status_code == 200:
        job_id = res.json()['id']
        return job_id
    else:
        handle_request_error(res)

def _job_done(job_id, is_finished, error_occurred, time_finished_pck):
    if not job_id:
        print_error("Job finished on an error due to incorrect job initializion.")
        notify_me("A job has finished on an exception due to incorrect senpy initialization."
                "The final details couldn't be transmitted to the server.")
        return
    body = {
        "time_finished_pck": _date_to_str(time_finished_pck),
        "is_finished": is_finished,
        "error_occurred": error_occurred
    }
    res = put(f"job/{job_id}/done", json=body)
    if 'python_error' in res or res.status_code != 200:
        notify_me("A job has finished on an exception."
                "The final details couldn't be transmitted to the server.")
        handle_request_error(res)


class EventLoop(object):
    """
    Non-blocking loop from https://stackoverflow.com/a/38317060
    """

    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False


class ntm:
    """
    ntm (NoTify Me) decorates an iterable and sends periodic updates.
    """
    def __init__(self, iterable, name="", current_iteration=0):
        self.iterable = iterable
        self.name = name
        self.current_iteration = current_iteration
        self.total_iteration = len(iterable)
        self.time_started = _now()
        self.interruption = None # The server sets this attr to an error string to stop the job
        self.job_id = _create_job(self.time_started, self.total_iteration, 
                    current_iteration=current_iteration, job_name=name)


    def _update_job(self):
        if not self.time_at_last_iteration:
            # if update is called before the first iteration time_at_last is undefined
            return
        if not self.job_id:
            print_error("Update failed due to incorrect job initializion.")
            return
        body = {
        "current_iteration": self.current_iteration,
        "time_at_last_iteration_pck": _date_to_str(self.time_at_last_iteration + timedelta(days=35))
        }
        res = put(f"job/{self.job_id}/update_job", json=body)
        if 'python_error' in res or res.status_code != 200:
            if 'python_error' not in res and res.status_code == 400 and 'stop' in res.json():
                # If a job has been running for too long it triggers a 400 error
                self.interruption = res.json()['failure']
            else:
                handle_request_error(res)


    def __iter__(self):
        self.time_at_last_iteration = _now()
        lp = EventLoop(5, self._update_job) # periodic update loop calling update_job

        try: 
            for obj in self.iterable:
                yield obj
                sleep(2)
                print(self.current_iteration)
                self.current_iteration += 1
                self.time_at_last_iteration = _now()
                if self.interruption:
                    raise RuntimeError(self.interruption)
        
        except Exception as e:
            # KeybordInterrupt is not catched here
            print_error(str(e))
        finally:
            lp.stop()

            # Call _job_done in finally because not all interruptions are catched by Exception
            is_finished = (self.current_iteration + 1) == self.total_iteration # curr iter starts at 0
            error_occurred = not is_finished
            _job_done(self.job_id, is_finished, error_occurred, _now())

