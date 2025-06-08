import json
from dacite import from_dict

from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from . import models
from fingerprint.models import Fingerprint as fingerprint_model
from fingerprint.fingerprint import Fingerprint as fingerprint_dataclass


# Create and save a validated Django model instance. TODO: Better validation, errors
def create_fingerprint_model(model_cls, data, fields=None):
    if fields is not None:
        filtered_data = {field: data.get(field) for field in fields}
    else:
        filtered_data = data

    instance = model_cls(**filtered_data)
    instance.full_clean()
    instance.save()
    return instance


# Parse JSON into a Fingerprint dataclass instance.
def create_fingerprint_instance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        fingerprint = from_dict(fingerprint_dataclass, data)
        return fingerprint


# Retrieve full Fingerprint instance and serialize related models to dictionaries.
def fetch_full_fingerprint(fingerprint_id):
    try:
        fingerprint = fingerprint_model.objects.select_related(
            'http_header',
            'behavioral',
            'display',
            'storage',
            'css_media_feature',
            'permissions_status',
            'graphics',
            'hardware',
            'browser',
            'network_connection',
            'time_zone',
            'media',
            'touch_pointer',
            'performance_timings',
            'ip',
            'canvas',
            'plugins',
            'encrypted_media_capabilities',
            'audio',
            'fonts'
        ).get(id=fingerprint_id)

        result = model_to_dict(fingerprint)

        related_fields = [
            'http_header', 'behavioral', 'display', 'storage', 'css_media_feature',
            'permissions_status', 'graphics', 'hardware', 'browser', 'network_connection',
            'time_zone', 'media', 'touch_pointer', 'performance_timings', 'ip',
            'canvas', 'plugins', 'encrypted_media_capabilities', 'audio', 'fonts'
        ]

        for field in related_fields:
            related_obj = getattr(fingerprint, field, None)
            result[field] = model_to_dict(related_obj) if related_obj else None

        print(json.dumps(result, indent=2))
        return fingerprint

    except ObjectDoesNotExist:
        return None


# Build and save all related Fingerprint component models.
def build_fingerprint_components(data):
    return {
        "ip": create_fingerprint_model(models.IP, data.get("ip", {}), ["ip_address", "details"]),
        "audio": create_fingerprint_model(models.Audio, data.get("audio", {}), ["audio_hash"]),
        "behavioral": create_fingerprint_model(models.Behavioral, data.get("behavioral", {}), [
            "typing_speed", "mouse_entropy", "keystroke_dynamics",
            "scroll_behavior", "url_changes", "time_of_visit_patterns"
        ]),
        "browser": create_fingerprint_model(models.Browser, data.get("browser", {}), [
            "vendor", "product_sub", "build_id", "private_mode"
        ]),
        "canvas": create_fingerprint_model(models.Canvas, data.get("canvas", {}), [
            "canvas_hash", "webgl_hash"
        ]),
        "css_features": create_fingerprint_model(models.CSSMediaFeature, data.get("css_features", {}), [
            "prefers_dark_scheme", "font_smoothing", "reduced_motion",
            "reduced_data", "forced_colors"
        ]),
        "display": create_fingerprint_model(models.Display, data.get("display", {}), [
            "screen_height", "screen_width", "color_depth",
            "device_pixel_ratio", "color_gamut"
        ]),
        "fonts": create_fingerprint_model(models.Fonts, data.get("fonts", {}), ["installed_fonts"]),
        "graphics": create_fingerprint_model(models.Graphics, data.get("graphics", {}), [
            "webgl_renderer", "webgl_vendor", "webgl_extensions", "webgpu_adapter"
        ]),
        "hardware": create_fingerprint_model(models.Hardware, data.get("hardware", {}), [
            "os", "cpu_cores", "device_memory", "device_architecture"
        ]),
        "http_header": create_fingerprint_model(models.HttpHeaderFingerprint, data.get("http_header_fingerprint", {}), [
            "header_count", "http_version", "tls_protocol",
            "tls_cipher_suite", "headers_present", "unusual_headers"
        ]),
        "media": create_fingerprint_model(models.Media, data.get("media", {}), [
            "audio_codecs", "video_codecs", "media_devices"
        ]),
        "network": create_fingerprint_model(models.NetworkConnection, data.get("network", {}), [
            "effective_type", "downlink", "rtt"
        ]),
        "performance": create_fingerprint_model(models.PerformanceTimings, data.get("performance", {}), [
            "timings", "memory", "network_timing"
        ]),
        "permissions": create_fingerprint_model(models.PermissionsStatus, data.get("permissions", {}), [
            "geolocation", "notifications", "camera", "microphone", "midi"
        ]),
        "plugins": create_fingerprint_model(models.Plugins, data.get("plugins", {}), [
            "installed_plugins", "mime_types"
        ]),
        "encrypted_media": create_fingerprint_model(models.EncryptedMediaCapabilities, data.get("encrypted_media_capabilities", {}), [
            "cdm_list"
        ]),
        "storage": create_fingerprint_model(models.Storage, data.get("storage", {}), [
            "cookies_enabled", "storage_estimate", "service_workers",
            "indexeddb_dbs", "cache_storage_keys"
        ]),
        "time_zone": create_fingerprint_model(models.TimeZone, data.get("time_zone", {}), [
            "time_zone", "timezone_offset", "languages"
        ]),
        "touch_pointer": create_fingerprint_model(models.TouchPointer, data.get("touch_pointer", {}), [
            "max_touch_points", "pointer_fine", "standalone"
        ])
    }


# Create the main Fingerprint model.
def create_fingerprint(data):
    components = build_fingerprint_components(data)

    fingerprint = models.Fingerprint.objects.create(
        http_header=components["http_header"],
        behavioral=components["behavioral"],
        display=components["display"],
        storage=components["storage"],
        css_media_feature=components["css_features"],
        permissions_status=components["permissions"],
        graphics=components["graphics"],
        hardware=components["hardware"],
        browser=components["browser"],
        network_connection=components["network"],
        time_zone=components["time_zone"],
        media=components["media"],
        touch_pointer=components["touch_pointer"],
        performance_timings=components["performance"],
        ip=components["ip"],
        canvas=components["canvas"],
        plugins=components["plugins"],
        encrypted_media_capabilities=components["encrypted_media"],
        audio=components["audio"],
        fonts=components["fonts"],
    )
    return fingerprint