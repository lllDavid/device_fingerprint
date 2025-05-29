from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Order
from cart.models import Cart

@login_required(login_url=('login'))
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if not cart.cart_items.exists():
        return redirect('cart')

    if request.method == 'POST':
        total_price = cart.get_total_cart_price()
        shipping_cost = Decimal('10.00')
        tax_amount = Decimal('5.00')
        discount_amount = Decimal('0.00')

        order = Order(
            user=request.user,
            total_price=total_price,
            shipping_cost=shipping_cost,
            tax_amount=tax_amount,
            discount_amount=discount_amount,
            shipping_address=request.POST.get('shipping_address', ''),
            shipping_method=request.POST.get('shipping_method', 'Standard'),
            status='pending',
            payment_status='pending',
        )
        order.save()

        for item in cart.cart_items.all():
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            order_item.save()

        return redirect('order_confirmation', order_id=order.id)

    total_price = cart.get_total_cart_price()
    shipping_cost = Decimal('10.00')
    tax_amount = Decimal('5.00')
    discount_amount = Decimal('0.00')

    context = {
        'cart': cart,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'tax_amount': tax_amount,
        'discount_amount': discount_amount,
    }

    return render(request, 'order-checkout.html', context)
