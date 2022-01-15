from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path("<slug:slug>/", views.index_details, name="index_details"), #e_commerce details page
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
]