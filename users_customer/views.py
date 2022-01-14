from django.shortcuts import render
from .models import *
# Create your views here.


def index(request):
    totals = Product.get_all_products()
    
    categories = Category.get_all_categories()
   
    context = {

        'totals': totals,
        
        'categories': categories,
    }

    return render(request, 'users_customer/index.html', context)


#cart views creation
def cart(request):
    #if the user is authenticated
    if request.user.is_authenticated:
        #setting the customer value. Simply setting the customer to profile that has the user.
        profile = request.user.profile
        #creating an object or querying an object. Having setting the Order to the customer with complete status as false.
        profile = profile.save()
        order, created = Order.objects.get_or_create(profile=profile, complete=False)
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

    return render(request, 'users_customer/cart.html', context)


def checkout(request):
    context = {

    }
    return render(request, 'users_customer/checkout.html', context)

