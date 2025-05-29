import json
from django.db import models
from django.conf import settings


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    transaction_id = models.CharField(max_length=100, blank=True, null=True)

    payment_details = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Payment #{self.pk} by {self.user.email} - {self.amount} {self.status}"

    def is_successful(self):
        return self.status == 'completed'

    def is_failed(self):
        return self.status == 'failed'

    def process_payment(self):
        pass

    def get_payment_details(self):
        try:
            return json.loads(self.payment_details) if self.payment_details else {}
        except json.JSONDecodeError:
            return {}

    def set_payment_details(self, details: dict):
        self.payment_details = json.dumps(details)
