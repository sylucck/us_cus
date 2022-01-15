from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('<slug:slug>/', views.ProductDetail.as_view(), name='index_details'), #e_commerce details page
   
]