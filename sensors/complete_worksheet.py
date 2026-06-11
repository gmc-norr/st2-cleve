import os
from pathlib import Path
from st2common import log as logging
from st2reactor.sensor.base import PollingSensor

LOG = logging.getLogger(__name__)


class CompleteWorksheetSensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=60):
        super(CompleteWorksheetSensor, self).__init__(
            sensor_service, config, poll_interval
        )
        self._watched_directories = self.config.get("illumina_directories", [])
        self._log_file_suffix = self.config.get("log_suffix")
        LOG.debug("watched directories:")
        for wd in self._watched_directories:
            LOG.debug(f"  - {wd}")

    def setup(self):
        pass

    def poll(self):
        """
        Poll the file system for new run directories
        """
        automation_log_files = self.check_ongoing_automations()
        for log_file in automation_log_files:
            ok, completed_samples, failed_samples = self.complete_log_file(log_file)
            if not ok:
                LOG.info(f"{log_file} ongoing")
                continue
            test_profile = log_file.split("/")[-1][: - (len(self._log_file_suffix) + 1)]
            LOG.info(f"dispatching trigger cleve.complete_worksheet\n"
                     f"completed_samples: {completed_samples}\n"
                     f"failed_samples: {failed_samples}\n"
                     f"test_profile: {test_profile}"
                     )
            self.sensor_service.dispatch("cleve.complete_worksheet",
                                         {"completed_samples": list(completed_samples),
                                          "failed_samples": list(failed_samples),
                                           "test_profile": test_profile})
            os.rename(log_file, log_file + ".complete")

    def complete_log_file(self, log_file):
        """
        """
        completed_samples = set()
        failed_samples = set()
        with open(log_file, 'r') as file:
            for line in file:
                line = line.strip()
                if line.endswith('started'):
                    return False, completed_samples, failed_samples
                if line.endswith('failed'):
                    sample = line.split(" ")[0]
                    failed_samples.add(sample)
                elif line.endswith('completed'):
                    sample = line.split(" ")[0]
                    completed_samples.add(sample)
                else:
                    LOG.error(f"log file line has wrong format: {line}")   
        return True, completed_samples, failed_samples

    def check_ongoing_automations(self):
        automation_files = set()
        for wd in self._watched_directories:
            LOG.debug(f"checking watch directory: {wd}")
            if not os.path.exists(wd):
                LOG.error(f"directory {wd} does not exist")
                continue

            root, dirnames, _ = next(os.walk(wd))

            for dirname in dirnames:
                dirpath = Path(root) / str(dirname)
                files = os.listdir(dirpath)
                for file in files:
                    if file.endswith(self._log_file_suffix):
                        automation_files.add(str(dirpath/file))
        return automation_files

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
