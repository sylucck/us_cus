from django.db import models
from django.contrib.auth.models import User




# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=40, null=True, blank=True, help_text="Insert your name")
    image = models.ImageField(default='default.png', upload_to='profile_pics', null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)

    @staticmethod
    def get_all_users():
        return Customer.objects.all()

    def __str__(self):
        """String for representing a model object"""
        return self.name






class Category(models.Model):
    name = models.CharField(max_length=40, verbose_name='name')

    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    class  Meta:  #new
        verbose_name_plural  =  "Categories" 

    def __str__(self):
        """String for representing a model object"""
        return str(self.name)


class Product(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='product_image', null=True, blank=True)
    digital = models.BooleanField(default=False,null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,default=1)
    description = models.CharField(max_length=250, default='', null=True, blank=True)
    size = models.CharField(max_length=200, null=True, blank=True, help_text='Input size of product')

    def __str__(self):
        """String for representing a model object"""
        return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    



    class Meta:
        ordering = ['-name']

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("index_details", kwargs={"slug": str(self.slug)})
    
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
        
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		"""String for representing a model object"""
		return self.address





