import json
from dataclasses import asdict

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from fingerprint.helpers import create_fingerprint, create_fingerprint_instance, flatten_dict, fetch_full_fingerprint


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
            # Creates and saves the Fingerprint Django model instance in DB.
            fingerprint = create_fingerprint(data)
            print("Fingerprint from DB:",fetch_full_fingerprint(fingerprint.id))

        # Create a Fingerprint dataclass instance from the request
        # fingerprint_dataclass = create_fingerprint_instance(request)
        # print("\nFingerprint Dataclass",fingerprint_dataclass)

        # Convert the Fingerprint dataclass to a dictionary
        # fingerprint_dict = asdict(create_fingerprint_instance(request))
        # print("\nFingerprint Dictionary",fingerprint_dict)

        # Flatten the fingerprint dictionary
        # flattened_dict= flatten_dict(fingerprint_dict)
        # print("\nFingerprint Flattened Dict",flattened_dict)

        return JsonResponse({"status": "ok", "fingerprint_id": fingerprint.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)