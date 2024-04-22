from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length = 200, unique = True)
    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField()
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    discount = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to='products_pics')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank= True)
    description = models.CharField(max_length=200, null=True)
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    @property
    # Lay duong dan hinh
    def ImageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    @property
    def lastPrice(self):
        return self.price - (self.price * self.discount) / 100  
class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank= True)
    date_order = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default = False, null = True, blank = False)
    
    def __str__(self):
        return str(self.id)
    # Ham tra ve total items in Order 
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total    
    
        # Ham tra ve total price in Order 
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank= True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank= True)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    date_added = models.DateTimeField(auto_now_add = True   )
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE )
    body = models.TextField()
    date_added =  models.DateTimeField(auto_now_add = True   ) 
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default-avatar-icon-of-social-media-user-vector.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
