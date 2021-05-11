from requests import get
from requests.exceptions import ConnectionError


def get_current_ip() -> str:
    try:
        ip = get("https://api.ipify.org").text
    except ConnectionError:
        ip = "Not Connected to internet."
    return ip


sg_defaults = {
    "SG_IP_PROTOCOL": "tcp",
    "SG_FROM_PORT": 22,
    "SG_TO_PORT": 22,
    "SG_IP": get_current_ip() + "/32",
}
