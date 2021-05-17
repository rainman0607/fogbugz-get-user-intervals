import requests
import math
from ..tools.dateUtil import *
import os
import getpass

now = datetime.now()


def getToday():
    import config
    start = now.strftime("%Y-%m-%d 00:00:00Z")
    end = now.strftime("%Y-%m-%d 23:59:59Z")

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start,
        "dtEnd": end
    }

    response = requests.request("POST", "{}/api/listIntervals".format(config.api["endpoint"]), json=payload,
                                headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])

        arr.append(abs(dtEnd - dtStart).total_seconds())
    return "Today: " + str(round(sum(arr) / 60 / 60, 2)) + " hours"


def getWeek():
    import config
    dt = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start.strftime(("%Y-%m-%d %H:%M:%SZ")),
        "dtEnd": end.strftime(("%Y-%m-%d %H:%M:%S"))
    }

    response = requests.request("POST", "{}/api/listIntervals".format(config.api["endpoint"]), json=payload,
                                headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])
        arr.append(abs(dtEnd - dtStart).total_seconds())
    return "This week: " + str(round(sum(arr) / 60 / 60, 2)) + " hours"


def getMonth():
    import config
    todayDate = datetime.today()
    start = todayDate.replace(month=todayDate.month, day=1)
    endOfMonth = todayDate.replace(day=28) + timedelta(days=4)
    end = endOfMonth - timedelta(days=endOfMonth.day)

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start.strftime(("%Y-%m-%d 00:00:00Z")),
        "dtEnd": end.strftime(("%Y-%m-%d 00:00:00Z"))
    }

    response = requests.request("POST", "{}/api/listIntervals".format(config.api["endpoint"]), json=payload,
                                headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])
        arr.append(abs(dtEnd - dtStart).total_seconds())
    return "This month: " + str(round(sum(arr) / 60 / 60, 2)) + " hours"


def getMissing():
    import config
    dt = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start.strftime(("%Y-%m-%d %H:%M:%SZ")),
        "dtEnd": end.strftime(("%Y-%m-%d %H:%M:%S"))
    }

    response = requests.request("POST", "{}/api/listIntervals".format(config.api["endpoint"]), json=payload,
                                headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])
        arr.append(abs(dtEnd - dtStart).total_seconds())
    weekSum = round(sum(arr) / 60 / 60, 2)
    if weekSum >= config.etc['workHours']:
        return "You have worked " + str(weekSum) + " hours! That is " + str(
            round(weekSum - config.etc['workHours'], 2)) + " more hours than you needed too"
    else:
        return "You have worked " + str(weekSum) + " hours! You need to work " \
               + str(round(config.etc['workHours'] - weekSum, 2)) + " hours!"


def getAll():
    import config
    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
    }

    response = requests.request("POST", "{}/api/listIntervals".format(config.api["endpoint"]), json=payload,
                                headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])
        arr.append(abs(dtEnd - dtStart).total_seconds())
    return "All time: " + str(round(sum(arr) / 60 / 60, 2)) + " hours"


def setup():
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../config.py')
    if os.path.exists(path):
        action = input("Config file already exists, do you want to override it? Y/n: ")
        if action.lower() == "n":
            return "10-4!"

    endpoint = input("Insert your fogbugz url <https://your-subdomain.fogbugz.com>: ")
    email = input("E-mail: ")
    password = getpass.getpass('Password: ')
    workHours = input("Insert your work hours: ")
    if not "https://" in endpoint:
        endpoint = "https://" + endpoint

    payload = {
        "email": email,
        "password": password
    }

    headers = {
        "Content-Type": "application/json",
        "Origin": "",
        "X-Requested-With": ""
    }

    response = requests.request("POST", "{}/api/logon".format(endpoint), json=payload, headers=headers).json()
    if response['errors']:
        return print('\n{}'.format(response['errors'][0]['message']))

    token = response['data']['token']

    payload = {"token": token}
    response = requests.request("POST", "{}/api/viewPerson".format(endpoint), json=payload, headers=headers).json()
    ix = response['data']['person']['ixPerson']
    with open(path, 'w') as fp:
        fp.write('api = dict(\n')
        fp.write('	headers={\n')
        fp.write('		"Content-Type": "application/json",\n')
        fp.write('		"Origin": "",\n')
        fp.write('		"X-Requested-With": ""\n')
        fp.write('	},\n')
        fp.write('	endpoint="{}",\n'.format(endpoint))
        fp.write('	token="{}"\n'.format(token))
        fp.write(')\n\n')
        fp.write('etc = dict(\n')
        fp.write('	workHours={},\n'.format(workHours))
        fp.write('	ix={}\n'.format(ix))
        fp.write(')\n')

    return '\n{}'.format("Setup complete")
