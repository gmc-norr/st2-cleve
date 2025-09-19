from typing import Any, Dict, Optional, Tuple
import requests
from st2common.runners.base_action import Action


class CleveRequest(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = requests.Session()

    def run(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
        **kwargs,
    ) -> Tuple[bool, Dict[str, Any]]:
        if api_key is None:
            self.logger.info("using pack internal api key")
            api_key = self.config.get("api_key")
        req = self.generate_request(endpoint, method, params, data, api_key)
        self.logger.info(
            f"cleve request url={req.url} method={req.method} data={req.body}"
        )

        res = self.session.send(req)

        try:
            body = res.json()
        except requests.exceptions.JSONDecodeError:
            body = res.text

        if res.status_code != 200:
            self.logger.error(
                f"request failed status={res.status_code} body={res.text}"
            )
            return False, {
                "error": "cleve request failed",
                "status_code": res.status_code,
                "body": body,
            }
        return True, {
            "message": "cleve request succeeded",
            "status_code": res.status_code,
            "body": body,
        }

    def generate_request(
        self,
        endpoint: str,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        api_key: Optional[str] = None,
    ) -> requests.PreparedRequest:
        headers = {
            "Accept": "application/json",
        }
        if api_key is not None:
            headers["Authorization"] = api_key
        if method in ["POST", "PATCH", "PUT", "DELETE"]:
            headers["Content-Type"] = "application/json"

        clean_params = None
        if params is not None:
            clean_params = {}
            for k, v in params.items():
                if v:
                    clean_params[k] = v

        url = f"{self.config.get('base_url', '')}/api/{endpoint}"
        return requests.Request(
            url=url, method=method, params=clean_params, json=data, headers=headers
        ).prepare()
