from django.shortcuts import render, HttpResponse
from django.http import JsonResponse, request
from django.contrib.auth import authenticate, login, logout
from .form import CreateUserForm
from django.views.decorators.csrf import csrf_exempt
from .database import PostgreSQLDB
import io
from io import StringIO
import pandas as pd
import json

db = PostgreSQLDB(dbname='uibmogli', user='uibmogli', password='8ogImHfL_1G249lXtM3k2EAIWTRDH2mX')


# db.table_creation()
@csrf_exempt
def testing(request):
    return HttpResponse("Application is up")


@csrf_exempt
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Success")
        else:
            print('User Name or Password is incorrect')
            return HttpResponse('User Name or Password is incorrect')
    return HttpResponse("Login failed")


@csrf_exempt
def registerPage(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if form.is_valid():
                form.save()
                user_name = form.cleaned_data.get('username')
                password1 = form.cleaned_data.get('password1')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                address = request.POST.get('address')
                email = form.cleaned_data.get('email')
                mobile = request.POST.get('mobile')
                db.add_user(user_name, password1, first_name, last_name, address, email, mobile)
                return HttpResponse("Success")
            else:
                print(form.errors)
                return HttpResponse(str(form.errors))
        except Exception as e:
            print(e)
        return HttpResponse("Registration Failed1")


@csrf_exempt
def getuserdetails(request):
    return HttpResponse(json.dumps({"userinfo": list(db.get_user_data(request.POST.get("username")))}),
                        content_type="application/json")


@csrf_exempt
def googlelogin(request):
    username = request.POST.get("username")
    password = username + "@" + request.POST.get("id")
    email = request.POST.get("email")
    users = db.get_users()
    if username in users:
        return HttpResponse("Success")
    else:
        form = CreateUserForm({'username': username, 'email': email, 'password1': password})
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            db.add_user(user, email)
            return HttpResponse("Success")
        else:
            print(form.errors)
            return HttpResponse(str(form.errors))


@csrf_exempt
def logoutUser(request):
    pass



# File upload for rooms data
@csrf_exempt
def fileupload(request):
    try:
        files = request.FILES.get('file')
        if not files:
            return HttpResponse('No files uploaded', status=400)

        # Determine the file extension
        file_extension = files.name.split('.')[-1].lower()

        if file_extension == 'csv':
            # Read the CSV file content
            content = files.read().decode('utf-8')
            csv_data = io.StringIO(content)
            df = pd.read_csv(csv_data)
        elif file_extension == 'xlsx':
            # Read the Excel file content
            df = pd.read_excel(files)
        else:
            return HttpResponse('Unsupported file format. Please upload a CSV or XLSX file.', status=400)

        # Save the data to a CSV or Excel file
        file_name = 'data'
        if file_extension == 'csv':
            df.to_csv(f'{file_name}.csv', index=False)
        elif file_extension == 'xlsx':
            df.to_excel(f'{file_name}.xlsx', index=False)

        # Convert DataFrame to JSON format and return it as a response
        response_data = df.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

@csrf_exempt
def getdatawithinrange(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getroomsdata(request):
    df = pd.read_excel('Rooms_data.xlsx', engine='openpyxl')
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])
    # Extract the date part
    df['Date'] = df['TimeStamp'].dt.date

    from_date = request.POST.get('from_date')
    to_date = request.POST.get('to_date')
    from_date = pd.to_datetime(from_date).date()
    to_date = pd.to_datetime(to_date).date()
    facility = request.POST.get('facility')
    room = request.POST.get('room')
    df = df[(df["Facility"] == facility) & (df["Rooms"] == room)]
    df.drop(["Facility", "Rooms", "TimeStamp"], inplace=True, axis=1)
    result_df = df.groupby('Date').mean().reset_index()
    result_df = result_df[(result_df["Date"] >= from_date) & (result_df["Date"] <= to_date)]
    return HttpResponse(json.dumps({"rooms_data": result_df.to_json()}),
                        content_type="application/json")


@csrf_exempt
def getdatawithinrange(request):
    return HttpResponse("Under Dev")




# File upload for harvest data
@csrf_exempt
def fileupload(request):
    try:
        files = request.FILES.get('file')
        if not files:
            return HttpResponse('No files uploaded', status=400)

        # Determine the file extension
        file_extension = files.name.split('.')[-1].lower()

        if file_extension == 'csv':
            # Read the CSV file content
            content = files.read().decode('utf-8')
            csv_data = io.StringIO(content)
            df = pd.read_csv(csv_data)
        elif file_extension == 'xlsx':
            # Read the Excel file content
            df = pd.read_excel(files)
        else:
            return HttpResponse('Unsupported file format. Please upload a CSV or XLSX file.', status=400)

        # Save the data to a CSV or Excel file
        file_name = 'data'
        if file_extension == 'csv':
            df.to_csv(f'{file_name}.csv', index=False)
        elif file_extension == 'xlsx':
            df.to_excel(f'{file_name}.xlsx', index=False)

        # Convert DataFrame to JSON format and return it as a response
        response_data = df.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


    

    

@csrf_exempt
def getharvestdata(request):
    dataFrame = pd.read_csv("Harvest_data.csv")

    return HttpResponse(json.dumps({"harvest_data": dataFrame.to_json()}),
                        content_type="application/json")


@csrf_exempt
def getlayoutsectionadd(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getlayoutsectionread(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getlayoutsectionupdate(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getlayoutsectiondelete(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwareadd(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwareread(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwareupdate(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def gethardwaredelete(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwareadd(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwareread(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwareupdate(request):
    return HttpResponse("Under Dev")


@csrf_exempt
def getsoftwaredelete(request):
    return HttpResponse("Under Dev")
