from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from cart.models import Cart, CartItem
from product.models import Product


class ProductGridView(ListView):
    model = Product
    template_name = 'product-grid.html'
    context_object_name = 'products'

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product-detail.html'
    context_object_name = 'product'

    # Retrieve the stock quantity range for dynamic dropdown options
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        context['stock_range'] = range(1, product.stock + 1)
        return context

@login_required(login_url='login')
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  

    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    cart_item.quantity = quantity if created else cart_item.quantity + quantity
    
    cart_item.save()

    return HttpResponseRedirect(reverse('product-detail', args=[product_id]))

@login_required(login_url='login')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.cart.user == request.user:
        cart_item.delete()  

    return redirect('cart')  

def search_products(request):
    search_query = request.GET.get('q', '').strip()  

    if search_query:
        products = Product.objects.filter(name__iexact=search_query)  
    else:
        products = Product.objects.all()

    return render(request, 'product-grid.html', {'products': products, 'search_query': search_query})









