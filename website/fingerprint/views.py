import json

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from fingerprint.helpers import create_fingerprint

@csrf_exempt
def create_fingerprint_from_request(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        with transaction.atomic():
            fingerprint = create_fingerprint(data)

        return JsonResponse({"status": "ok", "fingerprint_id": fingerprint.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)