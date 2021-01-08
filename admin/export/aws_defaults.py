from requests import get


def get_current_ip() -> str:
    ip = get('https://api.ipify.org').text
    return ip


sg_defaults = {
                "SG_IP_PROTOCOL": 'tcp',
                "SG_FROM_PORT": 22,
                "SG_TO_PORT": 22,
                "SG_IP": get_current_ip() + '/32'
    }
