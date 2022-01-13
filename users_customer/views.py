from django.shortcuts import render
from .models import *
# Create your views here.


def index(request):
    totals = Product.get_all_products()
    tot_id = Customer.get_all_customers()
   
    context = {

        'totals': totals,
        'tot_id': tot_id,
    }

    return render(request, 'users_customer/index.html', context )
