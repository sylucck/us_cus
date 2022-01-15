from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import generic
# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=raw_password)
            #creating a customer with the user instances
            Customer.objects.create(user=user, name=username)
            #sending a success message
            messages.success(request, f'Hello {username}, your account has been created! You are able to log in')
            login(request, user)
            return redirect('login')

    else:
        form = UserRegistrationForm()
    return render(request, 'e_commerce/register.html', {'form':form})

def index(request):
    totals = Product.get_all_products()
    
    categories = Category.get_all_categories()
   
    context = {

        'totals': totals,
        
        'categories': categories,
    }

    return render(request, 'e_commerce/index.html', context)


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'e_commerce/index_details.html'


#cart views creation
def cart(request):
    #if the user is authenticated
    if request.user.is_authenticated:
        #setting the customer value. Simply setting the customer to profile that has the user.
        customer = request.user.customer
        #creating an object or querying an object. Having setting the Order to the customer with complete status as false.
        #customer = customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #we getting items attached to the order. we getting all order items that has the order.
        items = order.orderitem_set.all()
		#cartItems = order.get_cart_items
        # 
    else:
        #if user is not authenticated, we live an empty value.
        items = []

    context = {
        'items': items,
    }

    return render(request, 'e_commerce/cart.html', context)


def checkout(request):

    context = {

    }
    return render(request, 'e_commerce/checkout.html', context)

