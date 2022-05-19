import time
from typing import Optional

import requests
from requests import Response


def get_authorization(api_url, device_id) -> Optional[str]:
    authorize_url = api_url + f"/devices/{device_id}:knock"
    response = requests.get(authorize_url)
    try:
        return response.headers["Authorization"]
    except KeyError:
        pass


def send_measurement(api_url, token, device_id) -> Response:
    measure_url = api_url + f"/devices/{device_id}:measure"
    measurement = {"rco2": 5, "atmp": 5, "pm02": 5, "rhum": 5, "wifi": 5}
    headers = {"Authorization": token}
    response = requests.post(measure_url, json=measurement, headers=headers)
    return response


def main():
    server_url = "http://localhost:8080"
    api_url = server_url + "/api"
    device_id = "asdf"
    token = None
    while token is None:
        token = get_authorization(api_url, device_id)
        time.sleep(1)
    print(f"Got token:{token}")
    while True:
        response = send_measurement(api_url, token, device_id)
        if response.status_code >= 400:
            print(response.content)
        time.sleep(1)


if __name__ == "__main__":
    main()
