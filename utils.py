import os

from requests import request


def get_token():
    url = os.environ.get("API_URL")
    payload = {
        "username": os.environ.get("API_USERNAME"),
        "password": os.environ.get("API_PASSWORD"),
        "client_id": os.environ.get("API_CLIENT_ID") ,
        "client_secret": os.environ.get("API_CLIENT_SECRET"),
        "audience": os.environ.get("API_AUDIENCE"),
        "scope": "*",
        "grant_type": "password",
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    resp = request("POST", url, headers=headers, data=payload).json()
    return resp["access_token"]


def parse_scans(token, page=1, per_page=25):
    host = os.environ.get("API_AUDIENCE")
    url = f'{host}/api/v2/scans/get'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        "X-User-Id": "Auth0User",
        "X-Org-Id": "Auth0Org",
    }
    desired_year = True
    scans = []
    while desired_year:
        payload = {
            "Page": page,
            "PerPage": per_page,
        }
        resp = request("POST", url, headers=headers, json=payload).json()
        if not resp["Data"]:
            desired_year = False
        items = list(filter(lambda item: item["CreatedAt"].split('-')[0] == '2022', resp["Data"]))
        scans.extend(items)
        if len(items) < per_page:
            desired_year = False
        page += 1
    return scans


def parse_identities(token, id_list):
    host = os.environ.get("API_AUDIENCE")
    url = f'{host}/api/v2/identities/get'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}',
        "X-User-Id": "Auth0User",
        "X-Org-Id": "Auth0Org",
    }
    'Content-Type: application/json'
    payload = {
            "IDs": id_list
        }
    resp = request("POST", url, headers=headers, json=payload).json()
    return resp['Data']
