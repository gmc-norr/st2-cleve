from st2tests.base import BaseActionTestCase

from cleve_request import CleveRequest


class TestCleveRequest(BaseActionTestCase):
    action_cls = CleveRequest

    def setUp(self):
        super().setUp()
        self.action = self.get_action_instance(
            config={
                "base_url": "https://cleve",
                "api_key": "testkey",
            }
        )

    def test_add_run_request(self):
        req = self.action.generate_request(path="runs", method="POST")
        self.assertEqual(req.url, f"{self.action.config['base_url']}/api/runs")
        self.assertEqual(req.method, "POST")
        self.assertEqual(req.headers["Authorization"], self.action.config["api_key"])

    def test_api_key(self):
        req = self.action.generate_request(path="runs", method="POST", api_key="anotherkey")
        self.assertEqual(req.headers["Authorization"], "anotherkey")
