import requests
import math
from ..tools.dateUtil import *
import config

now = datetime.now()


def getToday():
    start = now.strftime("%Y-%m-%d 06:00:00Z")
    end = now.strftime("%Y-%m-%d 23:59:59Z")

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start,
        "dtEnd": end
    }

    response = requests.request("POST", config.api["endpoint"], json=payload, headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])

        arr.append(abs(dtEnd - dtStart).total_seconds())
    return "Today: " + str(math.ceil(round(sum(arr) / 60 / 60, 2))) + " hours"


def getWeek():
    dt = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start.strftime(("%Y-%m-%d %H:%M:%SZ")),
        "dtEnd": end.strftime(("%Y-%m-%d %H:%M:%S"))
    }

    response = requests.request("POST", config.api["endpoint"], json=payload, headers=config.api["headers"]).json()
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

    response = requests.request("POST", config.api["endpoint"], json=payload, headers=config.api["headers"]).json()
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
    dt = datetime.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d")
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)

    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
        "dtStart": start.strftime(("%Y-%m-%d %H:%M:%SZ")),
        "dtEnd": end.strftime(("%Y-%m-%d %H:%M:%S"))
    }

    response = requests.request("POST", config.api["endpoint"], json=payload, headers=config.api["headers"]).json()
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
    payload = {
        "token": config.api["token"],
        "ixPerson": config.etc["ix"],
    }

    response = requests.request("POST", config.api["endpoint"], json=payload, headers=config.api["headers"]).json()
    arr = []
    for interval in response['data']['intervals']:
        dtStart = parser.parse(interval["dtStart"])
        if not is_date(interval['dtEnd']):
            dtEnd = parser.parse(now.strftime(("%Y-%m-%d %H:%M:%SZ")))
        else:
            dtEnd = parser.parse(interval["dtEnd"])
        arr.append(abs(dtEnd - dtStart).total_seconds())
    return "All time: " + str(round(sum(arr) / 60 / 60, 2)) + " hours"
