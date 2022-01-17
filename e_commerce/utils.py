from .models import *
import json


def cookieCart(request):
        #Cookies cart items for guest users
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('Cart:', cart)
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping': False}
        cartItems = order['get_cart_items']
          

        
        
        for i in cart:
            #we use try: to prevent errors shown to the guest user when an item is deleted from the database
            try:

                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'imageURL':product.imageURL,

                },
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
                items.append(item)

                if product.digital == False:
                    order['shipping'] = True
            except:
                pass
        return {'cartItems': cartItems, 'order':order, 'items': items}

def cartData(request):
    #if the user is authenticated
    if request.user.is_authenticated:
        #setting the customer value. Simply setting the customer to profile that has the user.
        customer = request.user.customer
        #creating an object or querying an object. Having setting the Order to the customer with complete status as false.

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #we getting items attached to the order. we getting all order items that has the order.
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return {'cartItems': cartItems, 'order':order, 'items': items}