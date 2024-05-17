from django.shortcuts import render,redirect
from .models import Device, Unit, DailyArchive, MonthlyArchive
from rest_framework.authtoken.models import Token
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime


import json
import uuid

        
def get_devices(request, number):
    
    try:
        unit = Unit.objects.get(number = number)
        device = Device.objects.get(id = unit.device.id)
        reading = device.current_read
        vals = {
            "reading":reading,
            "price": round(reading * 0.25, 2),
            "quality": round(1.3 - unit.quality_level, 2)
        }

        return JsonResponse(vals, safe=False)
    except Exception as e:
            print(e)
            return JsonResponse({'error': 'Invalid unit number'}, status=401)





@csrf_exempt
def test_api(request):
    if request.method == 'PATCH':
        apiKey = request.headers.get('Authorization')
        body = json.loads(request.body)

        try:
            key = uuid.UUID(apiKey)
            device = Device.objects.get(api_key=key)
            device.current_read += body['reading']
            device.month_read += body['reading']
            device.save()
        except Device.DoesNotExist:
            return JsonResponse({'error': 'No device found'}, status=401)
        except ValueError:
            return JsonResponse({'error': 'Ivalid API Key'}, status=401)
    else:
        return 



@csrf_exempt
def getBill(request):
    if request.method == "POST":
        try:
            unit_number = json.loads(request.body)
            unit_number = unit_number['unit']
            unit = Unit.objects.get(number=unit_number)
            device = unit.device

            return JsonResponse([device.month_read], safe=False)
        except Unit.DoesNotExist:
            return JsonResponse({'error': 'No unit found'}, status=401)
        except Device.DoesNotExist:
            return JsonResponse({'error': 'No device found'}, status=401)
        except Exception as e:
            return JsonResponse({'error': "Error happened"}, status=401) 
        


@csrf_exempt
def update_devices(request):
    if request.method == 'PATCH':
        key = uuid.UUID(request.headers.get("Authorization"))
        try:
            data = json.loads(request.body)

            device = Device.objects.get(api_key=key)

            device.current_read = data['reading']

            device.save()
            
            return JsonResponse({"Success": "Updated devices"}, status=200)

        except Proxy.DoesNotExist:
            return JsonResponse({"Error": "No such proxy was found"})
    else:
        return JsonResponse({'status': 'error', 'message': 'Bad request'}, status=400)

def index(request):
    if request.method == 'GET':
        devices = Device.objects.all()
        for i in devices:
            i.current_read = 0
            i.save()
        
        return render(request, 'index.html',{'reading':0, 'price':0, 'error':False})


@csrf_exempt
def dailyData(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            device = Unit.objects.get(number = body['unit']).device
            archives = list(DailyArchive.objects.filter(device = device).values_list("total_reading", "date"))
            data = {'readings':[]}
            for reading,date in archives:
                data['readings'].append((reading, date.strftime("%A")))


            
            return JsonResponse(data, safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Unexpected error occured'}, status=400)
    else:
        return redirect("Dashboard")
    



@csrf_exempt
def monthlyData(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            device = Unit.objects.get(number = body['unit']).device
            archives = list(MonthlyArchive.objects.filter(device = device).values_list("total_reading", "month"))
            data = {'readings':[]}
            for reading,date in archives:
                data['readings'].append((reading, date))
            data['readings'].append((device.month_read, device.current_month))

            return JsonResponse(data, safe=False)

        except Exception as e:
            print(e)
            return JsonResponse({'status': 'error', 'message': 'Unexpected error occured'}, status=400)
    else:
        return redirect("Dashboard")





def byUnit(request, number):    
    try:
        unit = Unit.objects.get(number=number)
        device = Device.objects.get(id = unit.device.id)
        last_update = device.last_update

        today = datetime.datetime.now().date()
        if last_update.date() != today:
            device.current_read = 0
            device.save()
        reading = device.current_read
        price = round(reading * 0.25, 2)
        return render(request, 'index.html', {'reading':reading, 'price':price, 'error':False})
    except Exception:
        print("e")
        return render(request, 'index.html', {'error': True})


