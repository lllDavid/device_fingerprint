from django.db import models
from django.db.models import JSONField

class HttpHeaderFingerprint(models.Model):
    header_count = models.IntegerField(null=True, blank=True)
    http_version = models.CharField(max_length=20, null=True, blank=True)
    tls_protocol = models.CharField(max_length=50, null=True, blank=True)
    tls_cipher_suite = models.CharField(max_length=100, null=True, blank=True)
    headers_present = JSONField(default=list, null=True, blank=True)
    unusual_headers = JSONField(default=list, null=True, blank=True)
    referer = models.CharField(max_length=100, null=True, blank=True)

class Behavioral(models.Model):
    typing_speed = models.FloatField(null=True, blank=True)
    mouse_entropy = models.FloatField(null=True, blank=True)
    keystroke_dynamics = JSONField(default=dict, null=True, blank=True)
    scroll_behavior = JSONField(default=dict, null=True, blank=True)
    url_changes = JSONField(default=list, null=True, blank=True)
    time_of_visit_patterns = JSONField(default=list, null=True, blank=True)

class Display(models.Model):
    screen_height = models.IntegerField(null=True, blank=True)
    screen_width = models.IntegerField(null=True, blank=True)
    color_depth = models.IntegerField(null=True, blank=True)
    device_pixel_ratio = models.FloatField(null=True, blank=True)
    color_gamut = models.CharField(max_length=20, null=True, blank=True)

class Storage(models.Model):
    cookies_enabled = models.BooleanField(null=True, blank=True)
    storage_estimate = JSONField(default=dict, null=True, blank=True)
    service_workers = JSONField(default=list, null=True, blank=True)
    indexeddb_dbs = JSONField(default=list, null=True, blank=True)
    cache_storage_keys = JSONField(default=list, null=True, blank=True)

class CSSMediaFeature(models.Model):
    prefers_dark_scheme = models.BooleanField(null=True, blank=True)
    font_smoothing = models.BooleanField(null=True, blank=True)
    reduced_motion = models.BooleanField(null=True, blank=True)
    reduced_data = models.BooleanField(null=True, blank=True)
    forced_colors = models.BooleanField(null=True, blank=True)

class PermissionsStatus(models.Model):
    geolocation = models.CharField(max_length=20, null=True, blank=True)
    notifications = models.CharField(max_length=20, null=True, blank=True)
    camera = models.CharField(max_length=20, null=True, blank=True)
    microphone = models.CharField(max_length=20, null=True, blank=True)
    midi = models.CharField(max_length=20, null=True, blank=True)

class Graphics(models.Model):
    webgl_renderer = models.TextField(null=True, blank=True)
    webgl_vendor = models.TextField(null=True, blank=True)
    webgl_extensions = JSONField(default=list, null=True, blank=True)
    webgpu_adapter = JSONField(default=dict, null=True, blank=True)

class Hardware(models.Model):
    os = models.CharField(max_length=200, null=True, blank=True)
    cpu_cores = models.IntegerField(null=True, blank=True)
    device_memory = models.FloatField(null=True, blank=True)
    device_architecture = models.CharField(max_length=50, null=True, blank=True)

class Browser(models.Model):
    browser = models.CharField(max_length=100, null=True, blank=True)
    engine = models.CharField(max_length=100, null=True, blank=True)
    build_id = models.CharField(max_length=100, null=True, blank=True)
    private_mode = models.BooleanField(null=True, blank=True)

class NetworkConnection(models.Model):
    effective_type = models.CharField(max_length=20, null=True, blank=True)
    downlink = models.FloatField(null=True, blank=True)
    rtt = models.IntegerField(null=True, blank=True)

class TimeZone(models.Model):
    time_zone = models.CharField(max_length=100, null=True, blank=True)
    timezone_offset = models.IntegerField(null=True, blank=True)
    languages = JSONField(default=list, null=True, blank=True)

class Media(models.Model):
    audio_codecs = JSONField(default=list, null=True, blank=True)
    video_codecs = JSONField(default=list, null=True, blank=True)
    media_devices = JSONField(default=list, null=True, blank=True)

class TouchPointer(models.Model):
    max_touch_points = models.IntegerField(null=True, blank=True)
    pointer_fine = models.BooleanField(null=True, blank=True)
    standalone = models.BooleanField(null=True, blank=True)

class PerformanceTimings(models.Model):
    timings = JSONField(default=dict, null=True, blank=True)
    memory = JSONField(default=dict, null=True, blank=True)
    network_timing = JSONField(default=dict, null=True, blank=True)
    framerate = models.FloatField(null=True, blank=True)

class IP(models.Model):
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    details = JSONField(default=dict, blank=True, null=True)

class Canvas(models.Model):
    canvas_hash = models.CharField(max_length=128, null=True, blank=True)
    webgl_hash = models.CharField(max_length=128, null=True, blank=True)

class Plugins(models.Model):
    installed_plugins = JSONField(default=list, null=True, blank=True)
    mime_types = JSONField(default=list, null=True, blank=True)

class EncryptedMediaCapabilities(models.Model):
    cdm_list = JSONField(default=list, null=True, blank=True)

class Audio(models.Model):
    audio_hash = models.CharField(max_length=128, null=True, blank=True)

class Fonts(models.Model):
    installed_fonts = JSONField(default=list, null=True, blank=True)

class Fingerprint(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    http_header = models.OneToOneField(HttpHeaderFingerprint, null=True, blank=True, on_delete=models.CASCADE)
    behavioral = models.OneToOneField(Behavioral, null=True, blank=True, on_delete=models.CASCADE)
    display = models.OneToOneField(Display, null=True, blank=True, on_delete=models.CASCADE)
    storage = models.OneToOneField(Storage, null=True, blank=True, on_delete=models.CASCADE)
    css_media_feature = models.OneToOneField(CSSMediaFeature, null=True, blank=True, on_delete=models.CASCADE)
    permissions_status = models.OneToOneField(PermissionsStatus, null=True, blank=True, on_delete=models.CASCADE)
    graphics = models.OneToOneField(Graphics, null=True, blank=True, on_delete=models.CASCADE)
    hardware = models.OneToOneField(Hardware, null=True, blank=True, on_delete=models.CASCADE)
    browser = models.OneToOneField(Browser, null=True, blank=True, on_delete=models.CASCADE)
    network_connection = models.OneToOneField(NetworkConnection, null=True, blank=True, on_delete=models.CASCADE)
    time_zone = models.OneToOneField(TimeZone, null=True, blank=True, on_delete=models.CASCADE)
    media = models.OneToOneField(Media, null=True, blank=True, on_delete=models.CASCADE)
    touch_pointer = models.OneToOneField(TouchPointer, null=True, blank=True, on_delete=models.CASCADE)
    performance_timings = models.OneToOneField(PerformanceTimings, null=True, blank=True, on_delete=models.CASCADE)
    ip = models.OneToOneField(IP, null=True, blank=True, on_delete=models.CASCADE)
    canvas = models.OneToOneField(Canvas, null=True, blank=True, on_delete=models.CASCADE)
    plugins = models.OneToOneField(Plugins, null=True, blank=True, on_delete=models.CASCADE)
    encrypted_media_capabilities = models.OneToOneField(EncryptedMediaCapabilities, null=True, blank=True, on_delete=models.CASCADE)
    audio = models.OneToOneField(Audio, null=True, blank=True, on_delete=models.CASCADE)
    fonts = models.OneToOneField(Fonts, null=True, blank=True, on_delete=models.CASCADE)
