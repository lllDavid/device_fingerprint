async function collectFingerprint() {
    // ---------- Helper Functions ----------
    async function sha256(str) {
        const buf = new TextEncoder().encode(str);
        const hashBuffer = await crypto.subtle.digest('SHA-256', buf);
        return Array.from(new Uint8Array(hashBuffer))
            .map(b => b.toString(16).padStart(2, '0'))
            .join('');
    }

    async function queryPermission(name) {
        if (!navigator.permissions) return null;
        try {
            const status = await navigator.permissions.query({ name });
            return status.state;
        } catch {
            return null;
        }
    }

    function getWebGLContext() {
        return document.createElement('canvas').getContext('webgl') ||
            document.createElement('canvas').getContext('experimental-webgl');
    }

    function extractOS(userAgent) {
        const win = userAgent.match(/Windows NT ([\d.]+)/);
        if (win) return `Windows ${win[1]}`;
        const mac = userAgent.match(/Mac OS X ([\d_]+)/);
        if (mac) return `macOS ${mac[1].replace(/_/g, ".")}`;
        const android = userAgent.match(/Android ([\d.]+)/);
        if (android) return `Android ${android[1]}`;
        const ios = userAgent.match(/iPhone OS ([\d_]+)/) || userAgent.match(/CPU OS ([\d_]+)/);
        if (ios) return `iOS ${ios[1].replace(/_/g, ".")}`;
        const linux = /Linux/.test(userAgent);
        if (linux) return "Linux";
        return "Unknown";
    }
    /* Slows down whole script, little entropy since most users are on 60
    function trackFPS(durationMs = 2000) {
        return new Promise(resolve => {
            let frameCount = 0;
            const startTime = performance.now();

            function countFrame(time) {
                frameCount++;
                const elapsedMs = time - startTime;
                if (elapsedMs < durationMs) {
                    requestAnimationFrame(countFrame);
                } else {
                    const elapsedSeconds = elapsedMs / 1000;
                    const avgFps = frameCount / elapsedSeconds;
                    resolve(avgFps);
                }
            }
            requestAnimationFrame(countFrame);
        });
    }
    */
    async function checkAudioCodec(codec) {
        if (!navigator.mediaCapabilities) return false;
        const result = await navigator.mediaCapabilities.decodingInfo({ type: 'file', audio: { contentType: codec } });
        return result.supported;
    }

    async function checkVideoCodec(codecString) {
        if (!('mediaCapabilities' in navigator)) return null;
        const config = {
            type: 'file',
            video: {
                contentType: codecString,
                width: 1920,
                height: 1080,
                bitrate: 5000000,
                framerate: 30
            }
        };
        try {
            const result = await navigator.mediaCapabilities.decodingInfo(config);
            return result.supported;
        } catch {
            return null;
        }
    }

    async function getCanvasHash() {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = 187;
        canvas.height = 35;
        ctx.textBaseline = 'top';
        ctx.font = '14px Arial';
        ctx.fillStyle = '#f60';
        ctx.fillRect(125, 1, 62, 20);
        ctx.fillStyle = '#069';
        ctx.fillText('Canvas fingerprint', 2, 15);
        ctx.fillStyle = 'rgba(102,204,0,0.7)';
        ctx.fillText('Canvas fingerprint', 4, 17);
        const dataUrl = canvas.toDataURL();
        return await sha256(dataUrl);
    }

    async function getWebGLHash() {
        const c = document.createElement('canvas');
        const gl = c.getContext('webgl') || c.getContext('experimental-webgl');
        if (!gl) return null;
        c.width = 256;
        c.height = 256;
        gl.viewport(0, 0, c.width, c.height);
        gl.clearColor(0.1, 0.2, 0.3, 1);
        gl.clear(gl.COLOR_BUFFER_BIT);
        const pixels = new Uint8Array(c.width * c.height * 4);
        gl.readPixels(0, 0, c.width, c.height, gl.RGBA, gl.UNSIGNED_BYTE, pixels);
        return await sha256(Array.from(pixels).join(','));
    }

    async function getAvailableCDMs() {
        if (!navigator.requestMediaKeySystemAccess) return [];
        const keySystems = ['com.widevine.alpha', 'com.microsoft.playready', 'com.apple.fps.1_0'];
        const supportedCDMs = [];
        for (const keySystem of keySystems) {
            try {
                const config = [{
                    initDataTypes: ['cenc'],
                    videoCapabilities: [{ contentType: 'video/mp4; codecs="avc1.42E01E"' }]
                }];
                await navigator.requestMediaKeySystemAccess(keySystem, config);
                supportedCDMs.push(keySystem);
            } catch { }
        }
        return supportedCDMs;
    }

    async function getAudioHash() {
        return await new Promise(r => {
            try {
                const OfflineAudioContext = window.OfflineAudioContext || window.webkitOfflineAudioContext;
                const context = new OfflineAudioContext(1, 44100, 44100);
                const oscillator = context.createOscillator();
                const compressor = context.createDynamicsCompressor();
                oscillator.type = 'triangle';
                oscillator.frequency.setValueAtTime(10000, context.currentTime);
                compressor.threshold.setValueAtTime(-50, context.currentTime);
                compressor.knee.setValueAtTime(40, context.currentTime);
                compressor.ratio.setValueAtTime(12, context.currentTime);
                compressor.attack.setValueAtTime(0, context.currentTime);
                compressor.release.setValueAtTime(0.25, context.currentTime);
                oscillator.connect(compressor);
                compressor.connect(context.destination);
                oscillator.start(0);
                context.startRendering();
                context.oncomplete = async e => {
                    let sum = 0;
                    const buffer = e.renderedBuffer.getChannelData(0);
                    for (let i = 0; i < buffer.length; i++) sum += Math.abs(buffer[i]);
                    r(sum.toString());
                };
            } catch {
                r(null);
            }
        });
    }

    // ---------- Data Collection ----------

    // Empty values retrieved server side
    const http_header_fingerprint = {
        header_count: null,
        http_version: null,
        tls_protocol: null,
        tls_cipher_suite: null,
        headers_present: [],
        unusual_headers: [],
        referer: document.referrer
    };
    // TODO: Needs to be implemented
    const behavioral = {
        typing_speed: null,
        mouse_entropy: null,
        keystroke_dynamics: {},
        scroll_behavior: {},
        url_changes: [],
        time_of_visit_patterns: []
    };

    const display = {
        screen_height: window.screen.height,
        screen_width: window.screen.width,
        color_depth: window.screen.colorDepth,
        device_pixel_ratio: window.devicePixelRatio,
        color_gamut: ['rec2020', 'p3', 'srgb'].find(g =>
            window.matchMedia(`(color-gamut: ${g})`).matches
        ) || null
    };

    const storage_estimate = await (navigator.storage?.estimate?.() || Promise.resolve({ usage: 0, quota: 0 }));
    const service_worker_regs = await (navigator.serviceWorker?.getRegistrations?.() || []);
    const indexeddb_dbs = await (indexedDB.databases?.() || Promise.resolve([]));
    const caches_keys = await (caches?.keys?.() || Promise.resolve([]));

    const storage = {
        cookies_enabled: navigator.cookieEnabled,
        storage_estimate,
        service_workers: service_worker_regs.map(reg => reg.scope),
        indexeddb_dbs: indexeddb_dbs.map(db => db.name),
        cache_storage_keys: caches_keys
    };

    const css_features = {
        prefers_dark_scheme: window.matchMedia('(prefers-color-scheme: dark)').matches,
        font_smoothing: window.getComputedStyle(document.body).getPropertyValue('-webkit-font-smoothing') !== 'none',
        reduced_motion: window.matchMedia('(prefers-reduced-motion: reduce)').matches,
        reduced_data: window.matchMedia('(prefers-reduced-data: reduce)').matches,
        forced_colors: window.matchMedia('(forced-colors: active)').matches
    };

    const permissions = {
        geolocation: await queryPermission('geolocation'),
        notifications: await queryPermission('notifications'),
        camera: await queryPermission('camera'),
        microphone: await queryPermission('microphone'),
        midi: await queryPermission('midi')
    };

    const gl = getWebGLContext();
    let webgl_renderer = null, webgl_vendor = null, webgl_extensions = [];

    if (gl) {
        const isFirefox = navigator.userAgent.toLowerCase().includes("firefox");
        const debugInfo = !isFirefox ? gl.getExtension('WEBGL_debug_renderer_info') : null;
        webgl_renderer = debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);
        webgl_vendor = debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR);
        webgl_extensions = gl.getSupportedExtensions() || [];
    }

    let webgpu_adapter = {};
    if (navigator.gpu) {
        const adapter = await navigator.gpu.requestAdapter();
        if (adapter) {
            webgpu_adapter = {
                name: adapter.name || null,
                features: [...adapter.features],
                limits: adapter.limits || {},
                isFallbackAdapter: adapter.isFallbackAdapter || false
            };
        }
    }

    const graphics = {
        webgl_renderer,
        webgl_vendor,
        webgl_extensions,
        webgpu_adapter
    };

    const userAgent = navigator.userAgent;
    let device_architecture = null;

    if (/arm|aarch64/i.test(userAgent)) device_architecture = 'arm';
    else if (/x86_64|win64|wow64|x64|amd64/i.test(userAgent)) device_architecture = 'x86_64';

    const hardware = {
        os: extractOS(userAgent),
        cpu_cores: navigator.hardwareConcurrency || 0,
        device_memory: navigator.deviceMemory || 0,
        device_architecture
    };

    const browser = {
        browser: (() => {
            if (/OPR\/(\d+(\.\d+)?)/.test(userAgent)) return `Opera ${RegExp.$1}`;
            if (/Edg\/(\d+(\.\d+)?)/.test(userAgent)) return `Edge ${RegExp.$1}`;
            if (/Chrome\/(\d+(\.\d+)?)/.test(userAgent) && !/Edg|OPR/.test(userAgent)) return `Chrome ${RegExp.$1}`;
            if (/Firefox\/(\d+(\.\d+)?)/.test(userAgent)) return `Firefox ${RegExp.$1}`;
            if (/Version\/(\d+(\.\d+)?).*Safari/.test(userAgent)) return `Safari ${RegExp.$1}`;
            if (/MSIE (\d+(\.\d+)?)/.test(userAgent)) return `IE ${RegExp.$1}`;
            if (/Trident\/.*rv:(\d+(\.\d+)?)/.test(userAgent)) return `IE ${RegExp.$1}`;
            return "Unknown";
        })(),
        engine: (() => {
            if (/OPR|Edg|Chrome/.test(userAgent)) return "Blink";
            if (/Firefox/.test(userAgent)) return "Gecko";
            if (/Safari/.test(userAgent) && !/Chrome|Edg|OPR/.test(userAgent)) return "WebKit";
            if (/Trident|MSIE/.test(userAgent)) return "Trident";
            return "Unknown";
        })(),
        build_id: navigator.buildID || null,
        private_mode: null
    };

    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection || {};
    const network = {
        effective_type: connection.effectiveType || '',
        downlink: connection.downlink || 0,
        rtt: connection.rtt || 0
    };

    const timeZone = {
        time_zone: Intl.DateTimeFormat().resolvedOptions().timeZone || '',
        timezone_offset: new Date().getTimezoneOffset(),
        languages: navigator.languages || []
    };

    const audio_codecs = [];
    for (const c of [
        'audio/mp4; codecs="mp4a.40.2"',
        'audio/webm; codecs="opus"',
        'audio/ogg; codecs="vorbis"'
    ]) {
        if (await checkAudioCodec(c)) audio_codecs.push(c);
    }

    const video_codecs = [];
    for (const c of [
        'video/mp4; codecs="avc1.42E01E"',
        'video/webm; codecs="vp8"',
        'video/webm; codecs="vp9"',
        'video/ogg; codecs="theora"'
    ]) {
        if (await checkVideoCodec(c)) video_codecs.push(c);
    }

    let media_devices = [];
    if (navigator.mediaDevices?.enumerateDevices) {
        const devices = await navigator.mediaDevices.enumerateDevices();
        media_devices = devices.map(d => ({
            deviceId: d.deviceId,
            kind: d.kind,
            label: d.label,
            groupId: d.groupId
        }));
    }

    const media = { audio_codecs, video_codecs, media_devices };

    const touch_pointer = {
        max_touch_points: navigator.maxTouchPoints || 0,
        pointer_fine: window.matchMedia('(pointer: fine)').matches,
        standalone: window.matchMedia('(display-mode: standalone)').matches
    };

    const framerate = 0; // await trackFPS()
    const timings = performance.getEntriesByType('navigation')[0]?.toJSON() || {};
    const memory = performance.memory || {};
    const network_timing = performance.getEntriesByType('resource').reduce((acc, e) => {
        acc[e.name] = e.responseEnd - e.startTime;
        return acc;
    }, {});
    const performanceTimings = { timings, memory, network_timing, framerate };

    // Mock API Data
    const ipData = await Promise.resolve({
        ip: "192.0.2.1",
        city: "Testville",
        region: "Test Region",
        country_name: "Testland",
        postal: "12345",
        latitude: 45.0,
        longitude: -75.0,
        timezone: "UTC",
        asn: "AS12345",
        org: "TestOrg Inc.",
        currency: "TST",
        languages: "en,test"
    });

    const ip = {
        ip_address: ipData.ip || null,
        details: {
            city: ipData.city || null,
            region: ipData.region || null,
            country: ipData.country_name || null,
            postal_code: ipData.postal || null,
            latitude: ipData.latitude || null,
            longitude: ipData.longitude || null,
            timezone: ipData.timezone || null,
            asn: ipData.asn || null,
            organization: ipData.org || null,
            currency: ipData.currency || null,
            languages: ipData.languages || null
        }
    };

    /* Real API Data
      try {
          const res = await fetch('https://ipapi.co/json/');
          const data = await res.json();
     
          ip = {
              ip_address: data.ip || null,
              details: {
                  city: data.city || null,
                  region: data.region || null,
                  country: data.country_name || null,
                  postal_code: data.postal || null,
                  latitude: data.latitude || null,
                  longitude: data.longitude || null,
                  timezone: data.timezone || null,
                  asn: data.asn || null,
                  organization: data.org || null,
                  currency: data.currency || null,
                  languages: data.languages || null
              }
          };
      } catch (error) {
          console.error('Failed to get IP info:', error);
      }
    */

    const canvas = {
        canvas_hash: await getCanvasHash(),
        webgl_hash: await getWebGLHash()
    };

    const plugins = {
        installed_plugins: Array.from(navigator.plugins || []).map(p => p.name),
        mime_types: Array.from(navigator.mimeTypes || []).map(m => m.type)
    };

    const encrypted_media_capabilities = {
        cdm_list: await getAvailableCDMs()
    };

    const audio = {
        audio_hash: await getAudioHash()
    };

    const fonts = {
        installed_fonts: []
    };

    const fingerprint = {
        ip, audio, behavioral, browser, canvas, css_features, display,
        fonts, graphics, hardware, http_header_fingerprint, media, network,
        performance: performanceTimings, permissions, plugins,
        encrypted_media_capabilities, storage,
        time_zone: timeZone, touch_pointer
    };

    return fingerprint;
}

collectFingerprint().then(fp => {
    fetch("/fingerprint/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(fp)
    })
        .then(async response => {
            const contentType = response.headers.get("content-type") || "";
            const text = await response.text();
            if (contentType.includes("application/json")) {
                console.log("Server response:", JSON.parse(text));
            } else {
                console.warn("Expected JSON but got:", text);
            }
            console.log("Fingerprint:", fp);
        })
        .catch(error => console.error("Error sending fingerprint:", error));
});

