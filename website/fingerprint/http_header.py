from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class HttpHeaderFingerprint:
    header_count: Optional[int] = None
    http_version: Optional[str] = None
    tls_protocol: Optional[str] = None
    tls_cipher_suite: Optional[str] = None
    headers_present: List[str] = field(default_factory=list)
    unusual_headers: List[str] = field(default_factory=list)
    referer: Optional[str] = None


def create_http_header_fingerprint(request) -> HttpHeaderFingerprint:
    headers = request.headers
    header_count = len(headers)

    http_version = request.META.get('SERVER_PROTOCOL')

    tls_protocol = request.META.get('SSL_PROTOCOL')  
    tls_cipher_suite = request.META.get('SSL_CIPHER')

    headers_present = list(headers.keys())

    common_headers = {
        'accept', 'accept-encoding', 'accept-language', 'cache-control',
        'connection', 'cookie', 'host', 'pragma', 'referer', 'user-agent',
        'upgrade-insecure-requests'
    }

    unusual_headers = [h for h in headers_present if h.lower() not in common_headers]

    referer = headers.get('Referer')

    return HttpHeaderFingerprint(
        header_count=header_count,
        http_version=http_version,
        tls_protocol=tls_protocol,
        tls_cipher_suite=tls_cipher_suite,
        headers_present=headers_present,
        unusual_headers=unusual_headers,
        referer=referer
    )