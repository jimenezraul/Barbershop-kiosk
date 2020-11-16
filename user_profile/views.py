from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from photocrop.forms import PhotoForm
from photocrop.models import Photo
from barbershop.models import LogoImage, Barbers, Client
from .forms import AddressForm, AppointmentForm
from .models import Address, Appointment, Token
from django.contrib import messages
from .forms import UserUpdateForm
from barbershop.forms import NewBarber, BarberPhoto
from django.db.models import Q
from datetime import datetime, date, timedelta
import json
import datefinder
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import pytz
from .api import *
from django.http import HttpResponseRedirect


# scopes = ['https://www.googleapis.com/auth/calendar']

# json_data = 'static/client_secret.json'
# token = "static/token.pkl"
# flow = InstalledAppFlow.from_client_secrets_file(json_data, scopes=scopes)
# credentials = pickle.load(open(token, "rb"))
# service = build("calendar", "v3", credentials=credentials)

# result = service.calendarList().list().execute()

# calendar_id = result['items'][1]['id']

# result = service.events().list(calendarId=calendar_id,
#                                timeZone='America/New_York').execute()


@login_required(login_url='register')
def profile(request):
    clients = Client.objects.filter(user=request.user, completed=False)
    address = Address.objects.filter(user=request.user)
    if address.count() == 1:
        address = address[0]

    photoform = PhotoForm()
    user = User.objects.filter(username=request.user)[0]
    photos = Photo.objects.filter(user=request.user)
    if photos.count() == 1:
        photos = photos[0]
    context = {
        'user': user,
        'photoform': photoform,
        'photo': photos,
        'title': 'Profile',
        'address': address,
        'clients': clients,
    }
    return render(request, 'user_profile/profile.html', context)


@login_required(login_url='register')
def user_address(request):
    address = Address.objects.filter(user=request.user)
    instance = Address.objects.filter(user=request.user)
    if instance.count() == 1:
        instance = Address.objects.filter(user=request.user)[0]
        if request.method == 'POST':
            form = AddressForm(request.POST, instance=instance)
            if form.is_valid:
                form.save()
                messages.success(
                    request, "Your Info was successfully Updated!")
                return redirect('user-profile')
        else:
            form = AddressForm(instance=instance)
    else:
        if request.method == 'POST':
            form = AddressForm(request.POST, request.user)
            if form.is_valid:
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return redirect('user-profile')
        else:
            form = AddressForm()
    context = {
        'address': address,
        'form': form,
        'title': 'Address',
    }
    return render(request, 'user_profile/user_address.html', context)


@login_required(login_url='register')
def update_user_info(request, id):
    instance = User.objects.get(pk=id)
    logo = LogoImage.objects.filter(user=request.user)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST or None, instance=instance)
        if form.is_valid():
            instance.save()
            messages.success(request, "Your Info was successfully Updated!")
            return redirect('user-profile')

    form = UserUpdateForm(instance=instance)
    if logo.count() == 1:
        logo = logo[0]
    else:
        logo = None

    context = {
        'form': form,
        'logo': logo,
    }
    return render(request, "user_profile/update_user_info.html", context)


def time_slots(s_time, e_time):
    while s_time <= e_time:
        yield s_time.strftime("%I:%M%p")
        s_time += timedelta(minutes=30)


@login_required(login_url='register')
def barber_profile(request, id):
    barber = Barbers.objects.get(pk=id)
    today_month = datetime.now().date()
    anniversary = Barbers.objects.filter(user=request.user, hire_date__month=datetime.now().date().month,
                                         hire_date__day=datetime.now().date().day,).exclude(barber=barber)
    clients = Client.objects.filter(user=request.user, completed=False)
    clients = clients.filter(Q(barber=barber) | Q(barber='Any'))
    completed = Client.objects.filter(
        completed_by=barber).filter(date_completed=datetime.now())

    photoform = BarberPhoto()
    form = NewBarber(instance=barber)

    # anniversary_reminder = today_month - timedelta(days=-7)  <-- reminder a week before

    if not barber.hire_date:
        hire = 0
        years = 0
        happy_hire_day = ""
        happy_hire_greeting = ""
        hire = barber.hire_date
        todays_date = datetime.now().date()
        years_in_shop = ''
    else:
        hire = barber.hire_date
        todays_date = datetime.now().date()
        years_in_shop = barber.years_in_shop()
        if hire.day == todays_date.day and hire.month == todays_date.month:
            happy_hire_day = "Congratulations!"
            if years_in_shop == 1:
                happy_hire_greeting = f'Today you turn {years_in_shop} year in the Barbershop.'
            else:
                happy_hire_greeting = f'Today you turn {years_in_shop} years in the Barbershop.'
        else:
            happy_hire_day = ""
            happy_hire_greeting = ""

    if not barber.phone:
        area_code = "000"
        first_3_number = "000"
        last_4_number = "0000"
    else:
        area_code = barber.phone[0:3]
        first_3_number = barber.phone[3:6]
        last_4_number = barber.phone[6:]

    if barber.available == False:
        checkbox = "unchecked"
    else:
        checkbox = "checked"

    context = {
        "hire": hire,
        "todays_date": todays_date,
        "barbers": barber,
        "photoform": photoform,
        "clients": clients,
        "form": form,
        'checkbox': checkbox,
        "completed": completed,
        "area_code": area_code,
        "first_3_number": first_3_number,
        "last_4_number": last_4_number,
        "years_in_shop": years_in_shop,
        "happy_hire_day": happy_hire_day,
        'happy_hire_greeting': happy_hire_greeting,
        "anniversary": anniversary,
        "title": "Barber Profile",
    }
    return render(request, "user_profile/barber_profile.html", context)


@login_required(login_url='register')
def barber_status(request, id):
    ''' # Get info
    token = Token.objects.all()
    token = token[0].token
    setmore = Setmore()
    service = get_services(token, setmore.all_services)
    print(service["response"])

    # Is token is invalid refresh token
    if service["response"] == False:
        return redirect("update-token", id)
    for i in service["data"]["services"]:
        print(f"id: {i['key']}")
        print(f"Service: {i['service_name']}")
        print(f"Price: ${i['cost']}")
        print(f"Duration: {i['duration']} min")

    catergory_service = get_services(token, setmore.category_key, )
    '''

    barbers = Barbers.objects.get(pk=id)

    form = NewBarber(instance=barbers)

    if request.method == 'POST':
        form = NewBarber(request.POST or None, instance=barbers)
        if form.is_valid:
            form.save()
            messages.success(request, "Status Updated!")
            return redirect('barberprofile', id)

    if barbers.available == False:
        checkbox = "unchecked"
    else:
        checkbox = "checked"

    context = {
        'form': form,
        'barbers': barbers,
        'checkbox': checkbox,
    }
    return render(request, "user_profile/barber_status.html", context)


@login_required(login_url='register')
def barber_profile_update(request, id):
    barbers = Barbers.objects.get(pk=id)

    form = NewBarber(instance=barbers)

    number = barbers.phone

    if request.method == 'POST':
        form = NewBarber(request.POST or None, instance=barbers)
        if form.is_valid:
            form.save()
            messages.success(request, "Info Updated!")
            return redirect('barbershop-settings')

    context = {
        'form': form,
        'barbers': barbers,
        "number": number,

    }
    return render(request, "user_profile/barber_profile_update.html", context)


@login_required(login_url='register')
def create_appointment(request, id, time):
    barber = Barbers.objects.filter(pk=id)
    barber = barber[0]
    appt = Appointment()

    time = time
    appt.name = request.POST["name"]
    appt.date = request.POST['date']
    appt.time = time
    appt.barber = barber
    appt.user = request.user
    appt.save()

    '''
    if len(matches):
        start_time = matches[0]
        end_time = start_time + timedelta(minutes=duration)

    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/New_York',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 15},
            ],
        },
    }

    service.events().insert(calendarId=calendar_id, body=event).execute()
    '''
    return redirect('barberprofile', barber.id)


@login_required(login_url='register')
def appointment(request, id, time):
    barber = Barbers.objects.filter(pk=id)[0]
    form = AppointmentForm()
    context = {
        "barber": barber,
        "form": form,
        "time": time,
    }
    return render(request, "user_profile/create_appointment.html", context)


@login_required(login_url='register')
def update_token(request, id):
    barber = Barbers.objects.filter(pk=id)
    barber = barber[0]
    refresh_token_return = refresh_token(request, id=id)
    if "barber_profile/" in refresh_token_return:
        return redirect(refresh_token_return)
    else:
        return redirect("appointment-services", id)


def appointment_services(request, id):
    barber = Barbers.objects.get(pk=id)
    form = NewBarber(instance=barber)
    token = Token.objects.filter(user=request.user)
    if token:
        token = token[0].token

    # Get categories and if the response is false will redirect to refresh the token
    categories = get_service_by_category(token)
    if categories["response"] == False:
        return redirect("update-token", id)

    men_category = [i for i in categories["data"]["service_categories"]
                    if i["categoryName"] == "Men`s Haircut"][0]
    kid_category = [i for i in categories["data"]["service_categories"]
                    if i["categoryName"] == "Kid`s Haircut (12 yrs & under)"][0]
    other_category = [i for i in categories["data"]
                      ["service_categories"] if i["categoryName"] == "Other"][0]
    staff = get_staff(token)

    # Check if Barber's Name is in data and filtered
    staff = [i for i in staff["data"]["staffs"]
             if i["first_name"] == barber.barber]

    # Get the Barbers Key
    if staff:
        staff_key = staff[0]["key"]
    else:
        staff_key = None

    men_list = get_service_by_category_key(token, men_category["key"])
    men_list = [i for i in men_list["data"]["services"]
                if i["staff_keys"][0] == staff_key]
    kid_list = get_service_by_category_key(token, kid_category["key"])
    kid_list = [i for i in kid_list["data"]["services"]
                if i["staff_keys"][0] == staff_key]
    other_list = get_service_by_category_key(token, other_category["key"])
    other_list = [i for i in other_list["data"]
                  ["services"] if i["staff_keys"][0] == staff_key]

    # service_key = men_list[0]["key"]

    # slots = get_available_slots(token, staff_key, service_key, "11/06/2020")

    services = {
        "men_category": men_category["categoryName"],
        "men_list": men_list,
        "kid_category": kid_category["categoryName"],
        "kid_list": kid_list,
        "other_category": other_category["categoryName"],
        "other_list": other_list,
    }

    context = {
        "barber": barber,
        "services": services,
        "form": form,
        "staff_key": staff_key,
    }
    return render(request, "user_profile/appointment_services.html", context)


def appointment_slots(request, id, staff_key, service_key):
    barber = Barbers.objects.get(pk=id)
    date_selected = request.GET["date_picker"]
    token = Token.objects.filter(user=request.user)
    if token:
        token = token[0].token

    slots = get_available_slots(token, staff_key, service_key, date_selected)
    if slots["response"] == False:
        return redirect("update-token", id)

    morning = []
    afternoon = []
    evening = []
    for i in slots["data"]["slots"]:
        if i < "12":
            hour = datetime.strptime(i, '%H.%M')
            morning.append(hour)
        if i >= "12" and i < "16":
            hour = datetime.strptime(i, '%H.%M')
            afternoon.append(hour)
        if i >= "16":
            hour = datetime.strptime(i, '%H.%M')
            evening.append(hour)

    context = {
        "barber": barber,
        "slots": slots,
        "morning": morning,
        "afternoon": afternoon,
        "evening": evening,
    }
    return render(request, "user_profile/appointment_slots.html", context)


def appointment_date(request, id, staff_key, service_key):
    barber = Barbers.objects.get(pk=id)
    staff_key = staff_key
    service_key = service_key

    context = {
        "barber": barber,
        "staff_key": staff_key,
        "service_key": service_key,
    }
    return render(request, "user_profile/appointment_date.html", context)
