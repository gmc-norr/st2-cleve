import json
from unittest.mock import Mock
from st2tests.base import BaseActionTestCase

from cleve_request import CleveRequest


def mock_response(status_code, error=None):
    response = Mock()
    response.status_code = status_code
    if status_code == 200:
        result = {"message": "run_added", "run_id": "runxxx", "state": "pending"}
    if status_code == 401:
        result = {"error": "unauthorized", "message": "invalid API key"}
    else:
        result = {"message": "failed to add run", "error": error}
    response.text = json.dumps(result)
    response.json = Mock(return_value=result)
    return response


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

    def test_add_run_success(self):
        status = 200
        data = {"path": "/path/to/run"}
        self.action.session.send = Mock(return_value=mock_response(status))

        success, result = self.action.run(endpoint="runs", method="POST", data=data)
        self.assertTrue(success)
        self.assertEqual(result["status_code"], status)
        self.assertEqual(result["message"], "cleve request succeeded")
        self.action.session.send.assert_called()
        req = self.action.session.send.call_args.args[0]
        self.assertEqual(req.headers["Authorization"], self.action.config["api_key"])

    def test_add_run_internal_server_error(self):
        status = 500
        data = {"path": "/path/to/run"}
        self.action.session.send = Mock(
            return_value=mock_response(status, "random error")
        )

        success, result = self.action.run(endpoint="runs", method="POST", data=data)
        self.assertFalse(success)
        self.assertEqual(result["status_code"], status)
        self.assertEqual(result["error"], "cleve request failed")
        self.action.session.send.assert_called()
        req = self.action.session.send.call_args.args[0]
        self.assertEqual(req.headers["Authorization"], self.action.config["api_key"])

    def test_add_run_unauthorized(self):
        status = 401
        data = {"path": "/path/to/run"}
        self.action.session.send = Mock(
            return_value=mock_response(status, "random error")
        )

        success, result = self.action.run(
            endpoint="runs", method="POST", data=data, api_key="randomkey"
        )
        self.assertFalse(success)
        self.assertEqual(result["status_code"], status)
        self.assertEqual(result["error"], "cleve request failed")
        self.action.session.send.assert_called()
        req = self.action.session.send.call_args.args[0]
        self.assertEqual(req.headers["Authorization"], "randomkey")
