import json
from dataclasses import asdict

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from fingerprint.http_header import create_http_header_fingerprint

from fingerprint.helpers import create_fingerprint, create_fingerprint_instance, flatten_dict, fetch_full_fingerprint


def create_fingerprint_instance_with_http(request):
    fingerprint_instance = create_fingerprint_instance(request)
    http_header_fp = create_http_header_fingerprint(request)
    fingerprint_instance.http_header_fingerprint = http_header_fp
    return fingerprint_instance

@csrf_exempt
def create_fingerprint_from_request(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        http_header_fp = create_http_header_fingerprint(request)
        data['http_header_fingerprint'] = asdict(http_header_fp)
    
        with transaction.atomic():
            # Creates and saves the Fingerprint Django model instance in DB.
            fingerprint = create_fingerprint(data)
            print("Fingerprint from DB:",fetch_full_fingerprint(fingerprint.id))

        # Create a Fingerprint dataclass instance from the request
        # fingerprint_dataclass = create_fingerprint_instance_with_http(request)
        # print("\nFingerprint Dataclass",fingerprint_dataclass)

        # Convert the Fingerprint dataclass to a dictionary
        # fingerprint_dict = asdict(fingerprint_dataclass)
        # print("\nFingerprint Dictionary",fingerprint_dict)

        # Flatten the fingerprint dictionary
        # flattened_dict= flatten_dict(fingerprint_dict)
        # print("\nFingerprint Flattened Dict",flattened_dict)

        return JsonResponse({"status": "ok", "fingerprint_id": fingerprint.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)