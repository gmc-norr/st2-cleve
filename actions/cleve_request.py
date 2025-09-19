import requests
from st2common.runners.base_action import Action


class CleveRequest(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def run(self, url, method="GET", params=None, data=None, api_key=None):
        if api_key is None:
            self.logger.info("using pack internal api key")
            api_key = self.config.get("api_key")
        header = {
            "Authorization": api_key,
            "Accept": "application/json",
        }
        if method in ["POST", "PATCH", "PUT", "DELETE"]:
            header["Content-Type"] = "application/json"

        self.logger.info(f"cleve request url={url} method={method} data={data}")

        res = requests.request(method=method, url=url, params=params, json=data, headers=header)
        self.logger.info(f"status_code={res.status_code}")
        if res.status_code != 200:
            self.logger.error(f"request failed status={res.status_code} body={res.text}")
            try:
                body = res.json()
            except requests.exceptions.JSONDecodeError:
                body = res.text
            return False, {"error": "cleve request failed", "status_code": res.status_code, "body": body}

        return True, res.json()
