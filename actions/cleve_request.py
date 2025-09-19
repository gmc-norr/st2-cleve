from typing import Any, Dict, Optional, Tuple
import requests
from st2common.runners.base_action import Action


class CleveRequest(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def run(
        self,
        path: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        if api_key is None:
            self.logger.info("using pack internal api key")
            api_key = self.config.get("api_key")
        req = self.generate_request(path, method, params, data, api_key)
        self.logger.info(
            f"cleve request url={req.url} method={req.method} data={req.body}"
        )

        res = self.session.send(req)
        self.logger.info(f"status_code={res.status_code}")
        error = self.handle_error(res)
        if error is not None:
            self.logger.error(
                f"request failed status={res.status_code} body={res.text}"
            )
            return False, error
        return True, res.json()

    def handle_error(self, response: requests.Response) -> Optional[Dict[str, Any]]:
        if response.status_code != 200:
            try:
                body = response.json()
            except requests.exceptions.JSONDecodeError:
                body = response.text
            return {
                "error": "cleve request failed",
                "status_code": response.status_code,
                "body": body,
            }
        return None

    def generate_request(
        self,
        path: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
    ) -> requests.PreparedRequest:
        headers = {
            "Authorization": api_key,
            "Accept": "application/json",
        }
        if method in ["POST", "PATCH", "PUT", "DELETE"]:
            headers["Content-Type"] = "application/json"

        url = f"{self.config.get('base_url', '')}/api/{path}"
        return requests.Request(
            url=url, method=method, params=params, json=data, headers=headers
        ).prepare()
