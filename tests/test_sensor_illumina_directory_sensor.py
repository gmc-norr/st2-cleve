import mock
import os
from pathlib import Path
from st2tests.base import BaseSensorTestCase
import tempfile

from illumina_directory_sensor import IlluminaDirectorySensor


def mock_run_dir(path: str, runinfo: bool = True, runparameters: bool = True, excluded: bool = False):
    path = Path(path)
    path.mkdir()
    if runinfo:
        (path / "RunInfo.xml").touch()
    if runparameters:
        (path / "RunParameters.xml").touch()
    if excluded:
        (path / ".cleve_exclude").touch()


class IlluminaDirectorySensorTestCase(BaseSensorTestCase):
    sensor_cls = IlluminaDirectorySensor

    def setUp(self):
        super(IlluminaDirectorySensorTestCase, self).setUp()

        self.watch_directories = [
            tempfile.TemporaryDirectory(),
            tempfile.TemporaryDirectory(),
        ]

        self.sensor = self.get_sensor_instance(
            config={
                "base_url": "http://localhost:8080",
                "illumina_directories": [Path(d.name) for d in self.watch_directories],
                "exclude_marker": ".cleve_exclude",
                "required_files": ["RunInfo.xml", "RunParameters.xml"],
            }
        )

    def assert_trigger_dispatched(self, trigger, payload):
        for t in self.get_dispatched_triggers():
            if t["trigger"] == trigger:
                subset_payload = {k: t["payload"].get(k) for k in payload}
                if subset_payload == payload:
                    break
        else:
            raise AssertionError(
                f"trigger {trigger} with payload {payload} not dispatched"
            )

    def test_new_run_directory(self):
        registered_dirs = []
        self.sensor.registered_paths = mock.Mock(return_value=registered_dirs)

        # No triggers with no new directories
        self.sensor.poll()
        triggers = self.get_dispatched_triggers()
        assert len(triggers) == 0

        # Create new "run"
        new_dir_path = os.path.join(self.watch_directories[0].name, "run1")
        mock_run_dir(new_dir_path)

        # Single trigger should be dispatched
        self.sensor.poll()
        triggers = self.get_dispatched_triggers()
        assert len(triggers) == 1
        self.assert_trigger_dispatched("cleve.new_run_directory", {"path": new_dir_path})

        # Add run to database
        registered_dirs.append(new_dir_path)

        # No new triggers should be dispatched
        self.sensor.poll()
        triggers = self.get_dispatched_triggers()
        assert len(triggers) == 1

    def test_excluded_run_directory(self):
        self.sensor.registered_paths = mock.Mock(return_value=[])

        self.sensor.poll()
        triggers = self.get_dispatched_triggers()
        assert len(triggers) == 0

        # Create excluded run
        new_dir_path = os.path.join(self.watch_directories[1].name, "run2")
        mock_run_dir(new_dir_path, excluded=True)

        # No triggers should be emitted
        self.sensor.poll()
        assert len(triggers) == 0

    def test_invalid_run_directory(self):
        self.sensor.registered_paths = mock.Mock(return_value=[])

        self.sensor.poll()
        triggers = self.get_dispatched_triggers()
        assert len(triggers) == 0

        # Create invalid run
        new_dir_path = os.path.join(self.watch_directories[1].name, "run2")
        mock_run_dir(new_dir_path, runinfo=False)

        # No triggers should be emitted
        self.sensor.poll()
        assert len(triggers) == 0
