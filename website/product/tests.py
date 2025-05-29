from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Product
from decimal import Decimal
from django.utils import timezone


class ProductModelTestCase(TestCase):

    def setUp(self):
        # Create two sample products for testing ordering and update/deletion.
        self.product1 = Product.objects.create(
            name="Product One",
            description="First product description.",
            price="49.99",
            stock=20,
            categories=["books", "education"],
            metadata={"author": "Author One", "pages": 300}
        )
        self.product2 = Product.objects.create(
            name="Product Two",
            description="Second product description.",
            price="99.99",
            stock=15,
            categories=["electronics", "gadgets"],
            metadata={"brand": "BrandX", "warranty": "2 years"}
        )

    def test_product_creation(self):
        """
        Verify that products are created with the correct field values.
        """
        product = Product.objects.get(name="Product One")
        self.assertEqual(product.description, "First product description.")
        self.assertEqual(product.price, Decimal("49.99"))
        self.assertEqual(product.stock, 20)
        self.assertEqual(product.categories, ["books", "education"])
        self.assertEqual(product.metadata, {"author": "Author One", "pages": 300})
        self.assertIsNotNone(product.created_at)
        self.assertLessEqual(product.created_at, timezone.now())

    def test_default_values(self):
        """
        Ensure that default values are applied when categories and metadata are not provided.
        """
        product = Product.objects.create(
            name="Default Value Product",
            description="Testing default values.",
            price="29.99",
            stock=5,
        )
        self.assertEqual(product.categories, [])
        self.assertIsNone(product.metadata)

    def test_str_method(self):
        """
        Check that the __str__ method returns the product's name.
        """
        self.assertEqual(str(self.product1), "Product One")
        self.assertEqual(str(self.product2), "Product Two")

    def test_update_product(self):
        """
        Test updating product fields and persisting the changes.
        """
        product = self.product1
        product.price = "59.99"
        product.stock = 25
        product.categories.append("new category")
        product.metadata["pages"] = 350
        product.save()

        updated_product = Product.objects.get(id=product.id)
        self.assertEqual(updated_product.price, Decimal("59.99"))
        self.assertEqual(updated_product.stock, 25)
        self.assertIn("new category", updated_product.categories)
        self.assertEqual(updated_product.metadata["pages"], 350)

    def test_delete_product(self):
        """
        Test that a product can be deleted and is removed from the database.
        """
        product_id = self.product2.id
        self.product2.delete()
        with self.assertRaises(Product.DoesNotExist):
            Product.objects.get(id=product_id)

    def test_ordering_by_created_at(self):
        """
        Create products in a known order and check if ordering by created_at works.
        """
        # Create additional products
        product_a = Product.objects.create(
            name="Product A",
            description="Product A description.",
            price="10.00",
            stock=5,
        )
        product_b = Product.objects.create(
            name="Product B",
            description="Product B description.",
            price="20.00",
            stock=10,
        )

        # Order products by creation time (assuming auto_now_add assigns increasing timestamps)
        products = list(Product.objects.order_by('created_at'))
        self.assertEqual(products[0].name, self.product1.name)
        # The last product should be the most recently created one.
        self.assertEqual(products[-1].name, product_b.name)

    def test_json_field_storage(self):
        """
        Test that JSONField correctly stores and retrieves complex data.
        """
        data = {
            "dimensions": {"width": 10, "height": 20},
            "features": ["waterproof", "lightweight"]
        }
        product = Product.objects.create(
            name="JSON Test",
            description="Testing JSON field.",
            price="59.99",
            stock=12,
            metadata=data
        )
        retrieved = Product.objects.get(id=product.id)
        self.assertEqual(retrieved.metadata, data)

    def test_array_field_behavior(self):
        """
        Test that the ArrayField stores and retrieves list data correctly.
        """
        categories = ["fashion", "accessories", "sale"]
        product = Product.objects.create(
            name="Array Test",
            description="Testing ArrayField.",
            price="39.99",
            stock=30,
            categories=categories
        )
        retrieved = Product.objects.get(id=product.id)
        self.assertEqual(retrieved.categories, categories)
