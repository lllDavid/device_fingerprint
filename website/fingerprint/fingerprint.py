from dataclasses import dataclass, field


@dataclass
class HttpHeaderFingerprint:
    header_count: int | None                                    # Total number of HTTP headers sent // Server side
    http_version: str | None                                    # HTTP version used  // *
    tls_protocol: str | None                                    # TLS protocol version // *
    tls_cipher_suite: str | None                                # TLS cipher suite // *
    headers_present : list[str] = field(default_factory=list)   # Set of header names present in the request // *
    unusual_headers: list[str] = field(default_factory=list)    # List of uncommon headers present  // *

@dataclass
class Behavioral:
    typing_speed: float | None                                           # Average typing speed // Server side
    mouse_entropy: float | None                                          # Mouse movement randomness measure // *
    keystroke_dynamics:  dict[str, float] = field(default_factory=dict)  # Keystroke timing info // *
    scroll_behavior: dict[str, float] = field(default_factory=dict)      # Scroll event metrics // *
    url_changes: list[str] = field(default_factory=list)                 # URLs visited during session // *
    time_of_visit_patterns: list[str] = field(default_factory=list)      # Behavioral time patterns // *

@dataclass
class Display:
    screen_height: int                 # The height of the screen in pixels // window.screen.height
    screen_width: int                  # The width of the screen in pixels // window.screen.width
    color_depth: int                   # Screen color depth in bits // screen.colorDepth
    device_pixel_ratio: float          # Ratio of physical pixels to CSS pixels // window.devicePixelRatio
    color_gamut: str | None            # Color gamut supported // const gamut = ['rec2020', 'p3', 'srgb'].find(g => window.matchMedia(`(color-gamut: ${g})`).matches); console.log(gamut); 

@dataclass
class Storage:
    cookies_enabled: bool                                              # Whether cookies are enabled // navigator.cookieEnabled
    storage_estimate: dict[str, object] = field(default_factory=dict)  # Storage usage and quota estimates // navigator.storage.estimate()
    service_workers: list[str] = field(default_factory=list)           # List of registered Service Worker URLs // navigator.serviceWorker.getRegistrations()
    indexeddb_dbs: list[str] = field(default_factory=list)             # List of IndexedDB databases // indexedDB.databases()
    cache_storage_keys: list[str] = field(default_factory=list)        # List of Cache Storage keys // caches.keys()

@dataclass
class CSSMediaFeature:
    prefers_dark_scheme: bool            # Dark mode preference // window.matchMedia('(prefers-color-scheme: dark)').matches
    font_smoothing: bool                 # Font smoothing enabled // window.getComputedStyle(document.body).getPropertyValue('-webkit-font-smoothing')
    reduced_motion: bool                 # Reduced motion preference // window.matchMedia('(prefers-reduced-motion: reduce)').matches
    reduced_data: bool | None            # Reduced data usage preference // window.matchMedia('(prefers-reduced-data: reduce)').matches
    forced_colors: bool | None           # Forced colors mode // window.matchMedia('(forced-colors: active)').matches

@dataclass
class PermissionsStatus:
    geolocation: str | None              # Permission status // navigator.permissions.query({ name: 'geolocation' })
    notifications: str | None            # Permission status // navigator.permissions.query({ name: 'notifications' })
    camera: str | None                   # Permission status // navigator.permissions.query({ name: 'camera' })
    microphone: str | None               # Permission status // navigator.permissions.query({ name: 'microphone' })
    midi: str | None                     # Permission status // navigator.permissions.query({ name: 'midi' })

@dataclass
class Graphics:
    webgl_renderer: str                                              # WebGL renderer // const gl = document.createElement('canvas').getContext('webgl') || document.createElement('canvas').getContext('experimental-webgl'); if (!gl) console.log("WebGL not supported"); else console.log("Renderer:", (gl.getExtension('WEBGL_debug_renderer_info') ? gl.getParameter(gl.getExtension('WEBGL_debug_renderer_info').UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER)));
    webgl_vendor: str                                                # WebGL vendor // const gl=document.createElement('canvas').getContext('webgl')||document.createElement('canvas').getContext('experimental-webgl');if(!gl)console.log("WebGL not supported");else{const debugInfo=gl.getExtension('WEBGL_debug_renderer_info');const vendor=debugInfo?gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL):gl.getParameter(gl.VENDOR);console.log("Vendor:",vendor);}
    webgl_extensions: list[str] = field(default_factory=list)        # Supported WebGL extensions // const webgl_extensions = (gl => gl ? gl.getSupportedExtensions() : null)(document.createElement('canvas').getContext('webgl') || document.createElement('canvas').getContext('experimental-webgl'));
    webgpu_adapter: dict[str, object] = field(default_factory=dict)  # WebGPU adapter properties // (async()=>navigator.gpu?(a=await navigator.gpu.requestAdapter())?{name:a.name||null,features:[...a.features],limits:a.limits||{},isFallbackAdapter:a.isFallbackAdapter||false}:null:null)();

@dataclass
class Hardware:
    os: str                            # Operating system name + version // navigator.userAgent
    cpu_cores: int                     # Number of logical CPU cores // navigator.hardwareConcurrency
    device_memory: float               # Amount of RAM in gigabytes // navigator.deviceMemory
    device_architecture: str | None    # Inferred from userAgent (e.g., "arm", "x86_64") // navigator.userAgent

@dataclass
class Browser:
    vendor: str                              # Browser vendor name // navigator.vendor
    product_sub: str | None                  # Product sub-version identifier // navigator.productSub
    build_id: str | None                     # Browser build identifier // navigator.buildID
    private_mode: bool | None                # Private/incognito mode status // TODO: Create custom script

@dataclass
class NetworkConnection:
    effective_type: str            # Effective connection type // navigator.connection.effectiveType
    downlink: float                # Approximate downlink speed in Mbps // navigator.connection.downlink
    rtt: int                       # Round-trip time estimate in ms // navigator.connection.rtt

@dataclass
class TimeZone:
    time_zone: str                                            # Time zone identifier // Intl.DateTimeFormat().resolvedOptions().timeZone
    timezone_offset: int                                      # Offset from UTC in minutes // new Date().getTimezoneOffset()
    languages: list[str] = field(default_factory=list)        # List of user preferred languages // navigator.languages

@dataclass
class Media:
    audio_codecs: list[str] = field(default_factory=list)              # Supported audio codecs // mediaCapabilities.decodingInfo()
    video_codecs: list[str] = field(default_factory=list)              # Supported video codecs // mediaCapabilities.decodingInfo()
    media_devices: list[dict[str, str]] = field(default_factory=list)  # Available media devices // navigator.mediaDevices.enumerateDevices()

@dataclass
class TouchPointer:
    max_touch_points: int                 # Maximum simultaneous touch points // navigator.maxTouchPoints
    pointer_fine: bool                    # Fine pointer input available // window.matchMedia('(pointer: fine)')
    standalone: bool                      # Standalone display-mode // window.matchMedia('(display-mode: standalone)')

@dataclass
class PerformanceTimings:
    timings: dict[str, object] = field(default_factory=dict)         # Performance timing metrics // performance.getEntriesByType('navigation')
    memory: dict[str, float] = field(default_factory=dict)           # Memory usage stats // performance.memory
    network_timing: dict[str, float] = field(default_factory=dict)   # Network timing metrics // performance.getEntriesByType('resource'

@dataclass
class IP:
    ip_address: str | None                                         # User's public IP address // Server side
    details: dict[str, object] = field(default_factory=dict)       # Additional IP-related details // Lookup via API

@dataclass
class Canvas:
    canvas_hash: str                    # 2D canvas fingerprint hash // (async()=>{const sha256=async str=>{const buf=new TextEncoder().encode(str);const hashBuffer=await crypto.subtle.digest('SHA-256',buf);return Array.from(new Uint8Array(hashBuffer)).map(b=>b.toString(16).padStart(2,'0')).join('')};const canvas=document.createElement('canvas');const ctx=canvas.getContext('2d');ctx.textBaseline='top';ctx.font='14px Arial';ctx.fillStyle='#f60';ctx.fillRect(125,1,62,20);ctx.fillStyle='#069';ctx.fillText('Canvas fingerprint',2,15);ctx.fillStyle='rgba(102,204,0,0.7)';ctx.fillText('Canvas fingerprint',4,17);const dataUrl=canvas.toDataURL();const hash=await sha256(dataUrl);console.log(hash)})();
    webgl_hash: str                     # WebGL canvas fingerprint hash // (async()=>{const sha256=async s=>{const buf=new TextEncoder().encode(s);const h=await crypto.subtle.digest('SHA-256',buf);return Array.from(new Uint8Array(h)).map(b=>b.toString(16).padStart(2,'0')).join('')};const c=document.createElement('canvas');const gl=c.getContext('webgl')||c.getContext('experimental-webgl');if(!gl)return console.log(null);c.width=256;c.height=256;gl.viewport(0,0,c.width,c.height);gl.clearColor(0.1,0.2,0.3,1);gl.clear(gl.COLOR_BUFFER_BIT);const p=new Uint8Array(c.width*c.height*4);gl.readPixels(0,0,c.width,c.height,gl.RGBA,gl.UNSIGNED_BYTE,p);console.log(await sha256(Array.from(p).join(',')))})();

@dataclass
class Plugins:
    installed_plugins: list[str] = field(default_factory=list)     # List of names of installed browser plugins // navigator.plugins()
    mime_types: list[str] = field(default_factory=list)            # Supported MIME types by browser plugins // navigator.mimeTypes()

@dataclass
class EncryptedMediaCapabilities:
    cdm_list: list[str] = field(default_factory=list)              # Available Content Decryption Modules // async function getAvailableCDMs(){const keySystems=['com.widevine.alpha','com.microsoft.playready','com.apple.fps.1_0'],supportedCDMs=[];for(const keySystem of keySystems){try{const config=[{initDataTypes:['cenc'],videoCapabilities:[{contentType:'video/mp4; codecs="avc1.42E01E"'}]}];await navigator.requestMediaKeySystemAccess(keySystem,config);supportedCDMs.push(keySystem)}catch{}}return supportedCDMs.length?supportedCDMs:null;}getAvailableCDMs().then(cdm_list=>{cdm_list?console.log('Available CDMs:',cdm_list):console.log('No CDMs available');});
    
@dataclass
class Audio:
    audio_hash: str                                                # Web Audio API fingerprint hash // (async()=>await new Promise(r=>{try{const A=window.OfflineAudioContext||window.webkitOfflineAudioContext,c=new A(1,44100,44100),o=c.createOscillator(),m=c.createDynamicsCompressor();o.type='triangle';o.frequency.setValueAtTime(1e4,c.currentTime);m.threshold.setValueAtTime(-50,c.currentTime);m.knee.setValueAtTime(40,c.currentTime);m.ratio.setValueAtTime(12,c.currentTime);m.attack.setValueAtTime(0,c.currentTime);m.release.setValueAtTime(.25,c.currentTime);o.connect(m);m.connect(c.destination);o.start(0);c.startRendering();c.oncomplete=e=>{let h=0,b=e.renderedBuffer.getChannelData(0);for(let i=0;i<b.length;i++)h+=Math.abs(b[i]);r(h.toString())}}catch(e){r(null)}}))();

@dataclass
class Fonts:
    installed_fonts: list[str] = field(default_factory=list)       # Installed system fonts // TODO: Create custom script

@dataclass
class Fingerprint:
    ip: IP
    audio: Audio
    behavioral: Behavioral
    browser: Browser
    canvas: Canvas
    css_features: CSSMediaFeature
    display: Display
    fonts: Fonts
    graphics: Graphics
    hardware: Hardware
    http_header_fingerprint: HttpHeaderFingerprint
    media: Media
    network: NetworkConnection
    performance: PerformanceTimings
    permissions: PermissionsStatus
    plugins: Plugins
    encrypted_media_capabilities: EncryptedMediaCapabilities
    storage: Storage
    time_zone: TimeZone
    touch_pointer: TouchPointer







