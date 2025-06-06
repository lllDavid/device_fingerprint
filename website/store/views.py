import json
from dacite import from_dict
from fingerprint import fingerprint

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def home_view(request):
    return render(request, 'home.html')

def about_view(request):
    return render(request, 'about.html')

def contact_view(request):
    return render(request, 'contact.html')

stored_fingerprint = None
fingerprint_instance = None

@csrf_exempt
def create_fingerprint(request):
    global stored_fingerprint, fingerprint_instance
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            stored_fingerprint = data

            fingerprint_instance = from_dict(data_class=fingerprint.Fingerprint, data=stored_fingerprint)
            print(fingerprint_instance)

            return JsonResponse({"status": "ok"})
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Only POST allowed"}, status=405)