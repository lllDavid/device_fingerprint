from django.test import TestCase
from django.contrib.auth import get_user_model
from product.models import Product
from .models import Cart, CartItem


class CartModelTest(TestCase):
    def setUp(self):
        """Set up test data before each test runs."""
        # Create a test user with username, email, and password
        self.user = get_user_model().objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password"
        )

        # Create test products (ensuring stock is provided)
        self.product1 = Product.objects.create(name="Product 1", price=10.0, stock=100)
        self.product2 = Product.objects.create(name="Product 2", price=20.0, stock=50)

        # Create a cart for the user
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_creation(self):
        """Test that the cart is created and associated with the correct user."""
        self.assertEqual(self.cart.user, self.user)
        self.assertTrue(self.cart.is_active)
        self.assertEqual(str(self.cart), f"Cart for {self.user.email} - {self.cart.created_at}")

    def test_get_total_cart_price_empty(self):
        """Test that the total cart price is 0 when no items are in the cart."""
        self.assertEqual(self.cart.get_total_cart_price(), 0.0)

    def test_cart_with_items(self):
        """Test that the total cart price is calculated correctly when items are added."""
        # Add items to the cart
        cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)

        # Expected total: (2 * 10) + (1 * 20) = 40
        self.assertEqual(self.cart.get_total_cart_price(), 40.0)

    def test_cart_item_creation(self):
        """Test that a CartItem is correctly created and linked to a cart."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=3)

        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.product1)
        self.assertEqual(cart_item.quantity, 3)
        self.assertEqual(str(cart_item), f"3 x {self.product1.name} - Total: {cart_item.get_total_items_price()}")

    def test_get_total_items_price(self):
        """Test that the total price for a cart item is correctly calculated."""
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=4)

        # Expected total: 4 * 10 = 40
        self.assertEqual(cart_item.get_total_items_price(), 40.0)

    def test_cart_is_active_default(self):
        """Test that carts are active by default."""
        self.assertTrue(self.cart.is_active)
