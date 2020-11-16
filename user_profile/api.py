import http.client
import ssl
import json
from .models import Token, SetmoreAPI
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from barbershop.models import LogoImage, Barbers, Client


class Setmore():
    categoryKey = ""
    all_services = "/api/v1/bookingapi/services"
    category = "/api/v1/bookingapi/services/categories"
    category_key = f"/api/v1/bookingapi/services/categories/{categoryKey}"
    staff = "/api/v1/bookingapi/staffs"


def refresh_token(request, id):
    barber = Barbers.objects.filter(pk=id)[0]
    setmore_key = SetmoreAPI.objects.filter(user=request.user)
    if setmore_key:
        setmore_key = setmore_key[0].token_key
    else:
        messages.warning(request, "You have no API Key for Setmore")
        data = barber.get_absolute_url
        return data
    api_token = Token()
    token = Token.objects.all()
    conn = http.client.HTTPSConnection("developer.setmore.com")
    conn.request(
        "GET", f"/api/v1/o/oauth2/token?refreshToken={setmore_key}", context = ssl._create_unverified_context())
    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)
    data = data["data"]["token"]["access_token"]
    if token.count() == 1:
        api_token = token[0]
    api_token.token = data
    api_token.user = request.user
    api_token.save()
    return data


def get_services(api_token, url_get, categoryKey=None):
    conn = http.client.HTTPSConnection("developer.setmore.com", context = ssl._create_unverified_context())

    headers = {
        'content-type': "application/json",
        'authorization': f'Bearer {api_token}'
    }

    conn.request("GET", url_get,
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)

    return data


def get_service_by_category(api_token):
    conn = http.client.HTTPSConnection("developer.setmore.com", context = ssl._create_unverified_context())

    headers = {
        'content-type': "application/json",
        'authorization': f'Bearer {api_token}'
    }

    conn.request("GET", "/api/v1/bookingapi/services/categories",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)

    return data


def get_service_by_category_key(api_token, categoryKey):
    conn = http.client.HTTPSConnection("developer.setmore.com", context = ssl._create_unverified_context())

    headers = {
        'content-type': "application/json",
        'authorization': f'Bearer {api_token}'
    }

    conn.request("GET", f"/api/v1/bookingapi/services/categories/{categoryKey}",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)

    return data


def get_staff(api_token):
    conn = http.client.HTTPSConnection("developer.setmore.com", context = ssl._create_unverified_context())

    headers = {
        'content-type': "application/json",
        'authorization': f'Bearer {api_token}'
    }

    conn.request("GET", "/api/v1/bookingapi/staffs",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)

    return data


def get_available_slots(api_token, staff_key, service_key, selected_date):
    conn = http.client.HTTPSConnection("developer.setmore.com", context = ssl._create_unverified_context())

    headers = {
        'content-type': "application/json",
        'authorization': f'Bearer {api_token}'
    }

    params = {
        "staff_key": staff_key,
        "service_key": service_key,
        "selected_date": selected_date,
        "off_hours": False,
        "double_booking": False,
        "slot_limit": 30,
        "timezone": "America/New_York"
    }

    data = json.dumps(params)

    conn.request("POST", "/api/v1/bookingapi/slots", data,
                 headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data = json.loads(data)

    return data
