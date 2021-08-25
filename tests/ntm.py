from time import sleep 
from datetime import datetime
from senpy import ntm
import unittest
from senpy.request_utils import get
from dateutil.parser import parse
from datetime import datetime
from django.utils import timezone

class TestNTM(unittest.TestCase):

    def init_wrapper(self):
        self.wrapper = ntm(range(5), name='test', update_period=0.5)
        self.assertNotEqual(self.wrapper.job_id, None)
        self.job_id = self.wrapper.job_id

    def get_job(self, job_id):
        return get(f"job/{job_id}/get_job")

    def check_job_attr(self, current_iteration):
        """
        Get job information from server and check consistency or values
        """
        res_job = self.get_job(self.job_id)
        self.assertEqual(res_job.status_code, 200)
        job = res_job.json()
        self.assertEqual(job['job_name'], 'test')
        self.assertEqual(job['total_iteration'], 5)
        self.assertEqual(job['current_iteration'], current_iteration)
        self.assertGreater(datetime.now(tz=timezone.utc), parse(job['time_latest_update_serv']))

        if current_iteration == 0:
            self.assertGreater(parse(job['time_latest_update_serv']), parse(job['time_started_pck']))
        else:
            self.assertGreater(parse(job['time_at_last_iteration_pck']), parse(job['time_started_pck']))
            self.assertGreater(parse(job['time_latest_update_serv']), parse(job['time_at_last_iteration_pck']))

    def test_routine(self):
        """
        Test that the wrapper creation, update and closing work properly
        for the expected usage
        """
        self.init_wrapper()
        with self.wrapper as iterator:
            for i, item in enumerate(iterator):
                print("Update", i)
                sleep(1)
                self.check_job_attr(i) 
    
        sleep(1)
        res_job = self.get_job(self.job_id)
        self.assertEqual(res_job.status_code, 200)
        job = res_job.json()
        self.assertEqual(job['is_finished'], True)
        self.assertEqual(job['error_occurred'], False)

    def test_error(self):
        """
        Test that a job is ended properly when an exception
        occurs during the iteration
        """
        self.init_wrapper()
        #Assert that a Runtime error occurs
        with self.assertRaises(RuntimeError):
            with self.wrapper as iterator:
                for i, item in enumerate(iterator):
                    raise RuntimeError
        
        # Leaving the context manager on an exception should call job_done
        # with error_occurred as True
        sleep(1)
        res_job = self.get_job(self.job_id)
        self.assertEqual(res_job.status_code, 200)
        job = res_job.json()
        self.assertEqual(job['is_finished'], False)
        self.assertEqual(job['error_occurred'], True)       
        
    def test_interruption(self):
        """
        Test that the interruption flag from the server
        effectively stops the job
        """
        pass

if __name__ == '__main__':
    unittest.main()
