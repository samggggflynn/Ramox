import requests


true = True
false = False
null = None


def auto_request(url: str, req_type: str = 'POST', **kwargs) -> dict:
    res = requests.request(req_type, url, **kwargs)
    return eval(res.content.decode())