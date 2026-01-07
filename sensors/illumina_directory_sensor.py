import os
from pathlib import Path
import requests
from st2common import log as logging
from st2reactor.sensor.base import PollingSensor
from typing import List, Set

LOG = logging.getLogger(__name__)


class IlluminaDirectorySensor(PollingSensor):
    def __init__(self, sensor_service, config=None, poll_interval=60):
        super(IlluminaDirectorySensor, self).__init__(
            sensor_service, config, poll_interval
        )
        self._watched_directories = self.config.get("illumina_directories", [])

        LOG.debug("watched directories:")
        for wd in self._watched_directories:
            LOG.debug(f"  - {wd}")

    def setup(self):
        pass

    def poll(self):
        """
        Poll the file system for new run directories
        """
        new_run_dirs = self.check_new_runs()
        LOG.info(f"new directories: {new_run_dirs}")
        for path in new_run_dirs:
            LOG.info(f"dispatching trigger=cleve.new_run_directory path={path}")
            self.sensor_service.dispatch(
                "cleve.new_run_directory", {"path": path}
            )

    def check_new_runs(self) -> List[str]:
        """
        Check for new run directories within the watched directories.

        :param registered_rundirs: Existing run directories
        :type registered_rundirs: dict
        """
        disk_paths = self.potential_run_dirs()
        cleve_paths = self.registered_paths()
        new_dirs = disk_paths.difference(cleve_paths)
        return list(new_dirs)

    def potential_run_dirs(self) -> Set[str]:
        dirs = set()
        for wd in self._watched_directories:
            LOG.debug(f"checking watch directory: {wd}")
            if not os.path.exists(wd):
                LOG.error(f"directory {wd} does not exist")
                continue

            root, dirnames, _ = next(os.walk(wd))

            for dirname in dirnames:
                dirpath = Path(root) / str(dirname)
                dirs.add(str(dirpath))
        return dirs

    def registered_paths(self) -> Set[str]:
        paths = set()
        url = f"{self.config['base_url']}/api/runs"
        res = requests.get(url, params={
            "page_size": 0,
        })
        if res.status_code != 200:
            LOG.error(f"failed to get runs from cleve status={res.status_code} response={res.text}")
            return paths

        runs = res.json().get("runs", [])
        for run in runs:
            run_path = run.get("path")
            if run_path:
                paths.add(run_path)
        return paths

    def cleanup(self):
        pass

    def add_trigger(self, trigger):
        pass

    def update_trigger(self, trigger):
        pass

    def remove_trigger(self, trigger):
        pass
