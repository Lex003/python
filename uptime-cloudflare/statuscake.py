import requests

URL_STATUSCAKE_IPS = "https://app.statuscake.com/Workfloor/Locations.php?format=txt"
URL_CLOUDFLARE_ADD_IP = "https://api.cloudflare.com/client/" \
        "v4/user/firewall/access_rules/rules"


class APIError(Exception):
    pass


def load_ips():
    r = requests.get(URL_STATUSCAKE_IPS)
    ips = []
    for ip in r.text.split("\n"):
        if ip.strip():
            ips.append(ip.strip())

    return ips

def add_ip_to_cloudflare(ip, email, secret):
    headers = {
        "Content-Type": "application/json", 
        "X-Auth-Email": email,
        "X-Auth-Key": secret,
    }
    data = {
        "mode": "whitelist",
        "configuration": {
            "target": "ip",
            "value": ip,
        },
        "notes": "statuscake_ip",
    }
    r = requests.post(URL_CLOUDFLARE_ADD_IP, json=data, headers=headers)
    if not (r.status_code == 200 and r.json().get("success", False)):
        msg = "API returned error: {}"
        raise APIError(msg.format(r.json().get("errors", [])))

def ask_for_auth():
    input_function = None
    try:
        input_function = raw_input
    except NameError:
        input_function = input

    email = input_function("Email: ").strip()
    secret = input_function("API-Secret: ").strip()

    return email, secret

if __name__ == "__main__":
    auth = ask_for_auth()
    for ip in load_ips():
        add_ip_to_cloudflare(ip, *auth)

