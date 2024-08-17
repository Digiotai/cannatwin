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
    return HttpResponse(json.dumps({"userinfo": list(db.get_user_data(request.POST.get("email")))}),
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
        # Check if the request method is POST
        if request.method != 'POST':
            return HttpResponse('Invalid request method. Only POST is allowed.', status=405)
        
        # Get user email from request data ( it's passed as part of the request)
        email = request.POST.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Get the uploaded file
        files = request.FILES.get('file')
        if not files:
            return HttpResponse('No files uploaded', status=400)

        # Determine the file extension
        file_extension = files.name.split('.')[-1].lower()

        # Read file content based on the file extension
        if file_extension == 'csv':
            content = files.read().decode('utf-8')
            csv_data = io.StringIO(content)
            df = pd.read_csv(csv_data)
        elif file_extension == 'xlsx':
            df = pd.read_excel(files)
        else:
            return HttpResponse('Unsupported file format. Please upload a CSV or XLSX file.', status=400)

        # Save the data to the database using the store_file_data method
        db.store_file_data(email, df)

        # Convert DataFrame to JSON format and return it as a response
        response_data = df.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)


@csrf_exempt
def getdatawithinrange(request):
    return HttpResponse("Under Dev")




#Get rooms data api
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def getroomsdata(request):
    try:
        # Ensure the request method is GET
        if request.method != 'GET':
            return HttpResponse('Invalid request method. Only GET is allowed.', status=405)

        # Get the user email from the request parameters
        email = request.GET.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Fetch the uploaded data using the email
        uploaded_data = db.get_uploaded_data(email)

        # Check if any data was found
        if not uploaded_data:
            return JsonResponse({'message': 'No data found for the provided email.'}, status=404)

        # Return the data directly as JSON
        return JsonResponse(uploaded_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)



@csrf_exempt
def getdatawithinrange(request):
    return HttpResponse("Under Dev")



## For Harvest data
# File upload for harvest data
@csrf_exempt
def fileupload_harvest(request):
    try:
        # Check if the request method is POST
        if request.method != 'POST':
            return HttpResponse('Invalid request method. Only POST is allowed.', status=405)
        
        # Get user email from request data ( it's passed as part of the request)
        email = request.POST.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Get the uploaded file
        files = request.FILES.get('file')
        if not files:
            return HttpResponse('No files uploaded', status=400)

        # Determine the file extension
        file_extension = files.name.split('.')[-1].lower()

        # Read file content based on the file extension
        if file_extension == 'csv':
            content = files.read().decode('utf-8')
            csv_data = io.StringIO(content)
            df = pd.read_csv(csv_data)
        elif file_extension == 'xlsx':
            df = pd.read_excel(files)
        else:
            return HttpResponse('Unsupported file format. Please upload a CSV or XLSX file.', status=400)

        # Save the data to the database using the store_file_data method
        db.store_file_data(email, df)

        # Convert DataFrame to JSON format and return it as a response
        response_data = df.to_dict(orient='records')
        return JsonResponse(response_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)





#Get harvest data api
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def getharvestdata(request):
    try:
        # Ensure the request method is GET
        if request.method != 'GET':
            return HttpResponse('Invalid request method. Only GET is allowed.', status=405)

        # Get the user email from the request parameters
        email = request.GET.get('email')
        if not email:
            return HttpResponse('User email not provided.', status=400)

        # Fetch the uploaded data using the email
        uploaded_data = db.get_uploaded_data(email)

        # Check if any data was found
        if not uploaded_data:
            return JsonResponse({'message': 'No data found for the provided email.'}, status=404)

        # Return the data directly as JSON
        return JsonResponse(uploaded_data, safe=False)

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)





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
