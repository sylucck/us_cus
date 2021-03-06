from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import generic
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Q
# Create your views here.

#user registration page


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

#user profile page
def profile(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, 
                                   request.FILES,
                                   instance=request.user.customer)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            name = p_form.cleaned_data.get('name')
            messages.success(request,f' Hello {name}, Your account has been Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.customer)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'cartItems': cartItems,
    }
    return render(request, 'e_commerce/profile.html', context)

#store page
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
    
    totals = Product.get_all_products()
    page = request.GET.get('page', 1)

    paginator = Paginator(totals, 9)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    
    categories = Category.get_all_categories()
   
    context = {
        'users': users,
       
        'categories': categories,
        'cartItems': cartItems
    }

    return render(request, 'e_commerce/store.html', context)

#store details page
def product_details(request, slug):
    data = cartData(request)
    cartItems = data['cartItems']

    post = get_object_or_404(Product, slug=slug)
   
    context = {
        'post': post,
        'cartItems': cartItems,
    }      
    return render(request, 'e_commerce/product_details.html', context)

#category page
class CategoryListView(generic.ListView):
    model = Category
    template_name = 'e_commerce/category.html'
    #paginate_by = 10

    def get_context_data(self,**Kwargs):
        #call the base implementation first to get the context
        context = super(CategoryListView, self).get_context_data(**Kwargs)
        #Create any data and add it to the context
        context['category_list'] = Category.objects.all()
        return context

#category details page
def category_details(request, slug):
    data = cartData(request)
    cartItems = data['cartItems']

    cate = get_object_or_404(Category, slug=slug)
   
    context = {
        'cate': cate,
        'cartItems': cartItems,
    }      
    return render(request, 'e_commerce/category_details.html', context)




#cart page
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,
    }

    return render(request, 'e_commerce/cart.html', context)

#checkout page
def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
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

    #if order already exist, we want to change the quantity-add or substract not getting a new one
    orderItem, created  = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)




def processOrder(request):
    transaction_id  = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        

       
    else:

       customer, order = guestOrder(request, data)
        

            
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
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
    

    return JsonResponse("Payment complete", safe=False)


def searchposts(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton= request.GET.get('submit')

        if query is not None:
            search= Q(name__icontains=query) | Q(price__icontains=query)

            results= Product.objects.filter(search).distinct()

            context={'results': results,
                     'submitbutton': submitbutton,
                     'cartItems':cartItems }

            return render(request, 'search.html', context)

        else:
            return render(request, 'search.html', {'cartItems':cartItems})

    else:
        return render(request, 'search.html', {'cartItems':cartItems})


def about(request):
    abouts = About.objects.all()
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'e_commerce/about.html', {'abouts': abouts, 'cartItems':cartItems})
