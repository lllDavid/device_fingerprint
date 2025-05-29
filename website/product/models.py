import json
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    categories = models.TextField(default='')  
    metadata = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def get_categories(self):
        try:
            return self.categories.split(',') if self.categories else []
        except Exception:
            return []

    def set_categories(self, categories: list):
        self.categories = ','.join(categories)

    def get_metadata(self):
        try:
            return json.loads(self.metadata) if self.metadata else {}
        except json.JSONDecodeError:
            return {}

    def set_metadata(self, metadata: dict):
        self.metadata = json.dumps(metadata)
