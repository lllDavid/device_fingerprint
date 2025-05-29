from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import StoreUser  

def create_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = StoreUser.objects.create_user(email=email, username=username, password=password)

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)  
                return redirect('home') 
            else:
                messages.error(request, "Authentication failed. Please try again.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'registration/register.html')



'''
def create_superuser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_manager = StoreUser.objects  
        superuser = user_manager.create_superuser(email, username, password)
        return HttpResponse(f'Superuser {superuser.username} created successfully!')
    return render(request, 'create_superuser.html')
'''