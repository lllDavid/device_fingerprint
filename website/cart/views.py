from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Cart

@login_required(login_url='login')
def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(user=request.user)

    return render(request, 'cart.html', {'cart': cart})

