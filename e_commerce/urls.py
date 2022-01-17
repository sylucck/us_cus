from django.urls import path
from . import views
#user url configureation
from e_commerce import views as user_views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.index, name='index'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.cart, name='cart'),
    path('category/', views.category, name="category"),
    path('update_item/', views.updateItem, name='update_item'),
    path('process_order/', views.processOrder, name='process_order'),
    path('profile/', user_views.profile, name="profile"),
    path('register/', user_views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="e_commerce/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="e_commerce/logout.html"), name="logout"),
    #path('<category>/', views.CategoryDetail.as_view(), name='e_category'),
    path('category/<slug:slug>/', views.CategoryDetail.as_view(), name='category_details'),
    #path('<slug:slug>/', views.ProductDetail.as_view(), name='index_details'),#e_commerce details page
    path('<slug:slug>/', views.product_details, name='product_details')
    
    
]