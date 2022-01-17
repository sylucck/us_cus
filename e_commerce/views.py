from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import generic
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart
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
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
       cookieData = cookieCart(request)
       cartItems = cookieData['cartItems']
      
        
    totals = Product.get_all_products()
    
    categories = Category.get_all_categories()
   
    context = {

        'totals': totals,
        'categories': categories,
        'cartItems': cartItems
    }

    return render(request, 'e_commerce/index.html', context)


class ProductDetail(generic.DetailView):
    model = Product
    template_name = 'e_commerce/index_details.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']
        return super().dispatch(request, *args, **kwargs)


def category(request):
    cates = Category.get_all_categories

    context = {
        'cates': cates,
    }
    return render(request, 'e_commerce/category.html', context)

class CategoryDetail(generic.DetailView):
    model = Category
    template_name = 'e_commerce/category_details.html'



#cart views creation
def cart(request):
    #if the user is authenticated
    if request.user.is_authenticated:
        #setting the customer value. Simply setting the customer to profile that has the user.
        customer = request.user.customer
        #creating an object or querying an object. Having setting the Order to the customer with complete status as false.

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #we getting items attached to the order. we getting all order items that has the order.
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

          #if user is not authenticated, we live an empty value.
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'e_commerce/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'e_commerce/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('productid:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    #if order already exist, we want to change the quantity-add or substract not getiing a new one
    orderItem, created  = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)


    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES,
                                   instance=request.user.customer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f' Your account has been Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'e_commerce/profile.html', context)


def processOrder(request):
    transaction_id  = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        #items = order.orderitem_set.all()
        #cartItems = order.
        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order = order,
                address = data['shipping']['address'],
                city =data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode =data['shipping']['zipcode'],
            )
    else:
        print("user is not logged in..")
    return JsonResponse("Payment complete", safe=False)

