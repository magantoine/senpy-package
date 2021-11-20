from datetime import datetime, timezone, timedelta
from time import sleep
from types import GeneratorType

from .notifications import notify_me
from .request_utils import post, get, put, handle_request_error
from .account_manager import check_token_exists
from .user_token import get_token
from .cli import print_error
from datetime import datetime
from threading import Timer


END_ALERT_LOWER_BOUND = 1 ## in minutes

class EventLoop(object):
    """
    Non-blocking loop from https://stackoverflow.com/a/38317060. The method `_run` is periodically
    called with `self.interval` seconds in between
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


class ntm(object):
    """
    ntm (NoTify Me) decorates an iterable and sends periodic updates.
    It is implemented as a context manager to end the job properly 
    if the  iterator is interrupted (in __exit__). 
    More info: https://docs.python.org/3/reference/datamodel.html#with-statement-context-managers

    Attributes
    ----------
    iterable : an iterable object (required)
    name : name of the job (empty by default)
    current_iteration : iteration index at which you start the job (0 by default)
    update_period : number of iteration of the loop between each update (5 by defaults)
    disable_end_message : states if you want NTM to send you a message at the end or not (false by default)
    """
    def __init__(self, iterable, name="", current_iteration=0, update_period=5, disable_end_message=False, length=None):
        """
        Creates a NTM object to track your jobs

        Parameters
        ----------
        iterable : an iterable object (required)
        name : name of the job (empty by default)
        current_iteration : iteration index at which you start the job (0 by default)
        update_period : number of iteration of the loop between each update (5 by defaults)
        disable_end_message : states if you want NTM to send you a message at the end or not (false by default)

        Returns 
        -------
        A NTM object
        
        """
        # check that a token exists, if it doesn't exist, prompt register or login
        check_token_exists()
        self.iterable = iterable
        self.name = name
        self.current_iteration = current_iteration
        if length:
            self.total_iteration = length - 1
        else:
            if isinstance(iterable, GeneratorType):
                raise RuntimeError("You need to specify the total number of iteration (`length` parameter) when using a generator")
            self.total_iteration = len(iterable)
        self.time_started = self._now()
        self.interruption = None # The server sets this attr to an error string to stop the job
        self.job_id = self._create_job()
        self.update_period = update_period
        self.already_printed_warning = False
        self.disable_end_message = disable_end_message

        ## declaration of lp as None to initialize it
        self.lp = None

    def __iter__(self):
        """
        This method is called when starting a loop. It initializes a periodic update
        and then yields element one by one, keeping track of adequate information. 
        """
        self.time_at_last_iteration = self._now()
        self.lp = EventLoop(self.update_period, self._update_job) # periodic update loop calling update_job

        for item in self.iterable:
            yield item

            self.current_iteration += 1
            self.time_at_last_iteration = self._now()
            if self.interruption:
                # Raise error when interruption is a non-empty string
                raise RuntimeError(self.interruption)
    
    def __enter__(self):
        """
        This method is called when using `with ntm(...) as ...`
        What is returned by __enter__ will be assigned to what 
        follows `as` in the `with` statement
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        This method is called when leaving the `with` statement. Closing the job
        here ensures that it is done even if an exception occurs during an iteration. 
        """
        
        if(self.lp is not None):
            # may be called before __iter__
            self.lp.stop()
        is_finished = self.current_iteration == self.total_iteration
        error_occurred = not is_finished
        self._job_done(is_finished, error_occurred, self._now())

    def _date_to_str(self, date):
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _now(self):
        return datetime.now(tz=timezone.utc)

    def _create_job(self):
        body = {
            "time_started_pck": self._date_to_str(self.time_started),
            "total_iteration": self.total_iteration,
            "current_iteration": self.current_iteration,
            "job_name": self.name,
        }
        res = post("job/create_job", json=body)
        if 'python_error' not in res and res.status_code == 200:
            job_id = res.json()['id']
            return job_id
        else:
            handle_request_error(res)

    def _update_job(self):
        if get_token() is None:
            # Don't update if no token registered
            # That happens when a user logs out or deletes their account while a job is running
            # No error printed because the user is warned when logging out
            return
        if not self.time_at_last_iteration:
            # if update is called before the first iteration then time_at_last is undefined
            return
        if not self.job_id:
            # print_error("Update failed due to incorrect job initializion.")
            return
        body = {
        "current_iteration": self.current_iteration,
        "time_at_last_iteration_pck": self._date_to_str(self.time_at_last_iteration)
        }
        res = put(f"job/{self.job_id}/update_job", json=body)
        if 'python_error' in res or res.status_code != 200:
            if 'python_error' not in res and 'stop' in res.json():
                #E.g. if a job has been running for too long 
                self.interruption = res.json()['failure']
            else:
                #Don't print errors repeatedly in the update loop
                if not self.already_printed_warning:
                    handle_request_error(res)
                    self.already_printed_warning = True

    def _job_done(self, is_finished, error_occurred, time_finished_pck):
        if not self.job_id:
            print_error("Job finished on an error due to incorrect job initializion.")
            notify_me("A job has finished on an exception due to incorrect senpy initialization."
                    "The final details couldn't be transmitted to the server.")
            return
        body = {
            "time_finished_pck": self._date_to_str(time_finished_pck),
            "is_finished": is_finished,
            "error_occurred": error_occurred
        }
        res = put(f"job/{self.job_id}/done", json=body)
        if 'python_error' in res or res.status_code != 200:
            notify_me("A job has finished on an exception."
                    "The final details couldn't be transmitted to the server.")
            handle_request_error(res)
        else :
            ## if we get here that means the job is done properly
            starter = ""
            if(self.name == ""):
                starter = "A job"
            else :
                starter = f"The job {self.name}"
            
            timespan = round((self._now() - self.time_started).total_seconds())
            if(not self.disable_end_message and timespan > END_ALERT_LOWER_BOUND * 60):
                ## only superieur to 1 minutes
                notify_me(starter + f"is done (in {timespan} seconds) !")

