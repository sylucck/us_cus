from django.shortcuts import render
from .models import *
# Create your views here.


def index(request):
    totals = Product.get_all_products()
    tot_id = Customer.get_all_customers()
    categories = Category.get_all_categories()
   
    context = {

        'totals': totals,
        'tot_id': tot_id,
        'categories': categories,
    }

    return render(request, 'users_customer/index.html', context)

def cartData(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
		#cartItems = order.get_cart_items
        # 
    else:
        items = []

    context = {
        'items': items,
    }

    return render(request, 'users_customer/index.html', context)

