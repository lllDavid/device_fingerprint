import json
from unittest.mock import patch
from dataclasses import dataclass, asdict

from django.urls import reverse
from django.db import transaction
from django.test import TestCase, Client, RequestFactory

from fingerprint.models import Fingerprint
from fingerprint.helpers import create_fingerprint, flatten_dict
from fingerprint.views import create_fingerprint_instance_with_http


class FingerprintViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('create_fingerprint')

    def test_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
        self.assertIn("error", response.json())

    def test_invalid_json(self):
        response = self.client.post(self.url, data="invalid", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_valid_fingerprint_creation(self):
        valid_data = {
            "user_agent": "TestBrowser/1.0",
            "screen_resolution": "1920x1080",
            "timezone": "UTC",
        }

        response = self.client.post(
            self.url,
            data=json.dumps(valid_data),
            content_type="application/json",
            HTTP_USER_AGENT="TestBrowser/1.0"
        )

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn("fingerprint_id", json_response)

        fingerprint_id = json_response["fingerprint_id"]
        self.assertTrue(Fingerprint.objects.filter(id=fingerprint_id).exists())

    def test_invalid_content_type(self):
        valid_data = {
            "user_agent": "TestBrowser/1.0",
            "screen_resolution": "1920x1080",
            "timezone": "UTC"
        }

        response = self.client.post(
            self.url,
            data=json.dumps(valid_data),
            content_type="text/plain" 
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_create_fingerprint_saves_instance(self):
        data = {
            "user_agent": "TestBrowser/1.0",
            "screen_resolution": "1920x1080",
            "timezone": "UTC",
        }

        with transaction.atomic():
            fingerprint = create_fingerprint(data)

        self.assertIsInstance(fingerprint, Fingerprint)
        self.assertTrue(Fingerprint.objects.filter(id=fingerprint.id).exists())

    @patch('fingerprint.views.create_fingerprint_instance')
    @patch('fingerprint.views.create_http_header_fingerprint')
    def test_create_fingerprint_instance_with_http(self, mock_http_fp, mock_create_fp):
        request = RequestFactory().get('/')
        mock_http_fp.return_value = 'http_fp_value'
        mock_create_fp.return_value = type('FPInstance', (), {})()  

        setattr(mock_create_fp.return_value, 'http_header_fingerprint', None)

        result = create_fingerprint_instance_with_http(request)

        mock_create_fp.assert_called_once_with(request)
        mock_http_fp.assert_called_once_with(request)
        self.assertEqual(result.http_header_fingerprint, 'http_fp_value')

    def test_flatten_dict_flattens_nested_dict(self):
        nested = {
            "a": 1,
            "b": {
                "c": 2,
                "d": 3
            }
        }
        expected_flat = {
            "a": 1,
            "b.c": 2,
            "b.d": 3
        }
        result = flatten_dict(nested)
        self.assertEqual(result, expected_flat)


@dataclass
class DummyFingerprint:
    user_agent: str
    screen_resolution: str
    timezone: str


class DataclassConversionTests(TestCase):
    def test_asdict_conversion(self):
        fp_instance = DummyFingerprint("TestBrowser/1.0", "1920x1080", "UTC")
        fp_dict = asdict(fp_instance)

        self.assertIsInstance(fp_dict, dict)
        self.assertEqual(fp_dict["user_agent"], "TestBrowser/1.0")