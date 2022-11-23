
from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CategoryModel(models.Model):
    slug = models.CharField(max_length=120,null=False,blank=False)
    name = models.CharField(max_length=120,null=False,blank=False)
    # image = models.ImageField(upload_to="image/",null=True,blank=True)
    description = models.TextField(max_length=500,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0=defual,1=hidden")
    trending = models.BooleanField(default=False,help_text="0=defual,1=hidden")
    meta_title = models.CharField(max_length=140,null=False,blank=True)
    meta_keyword = models.CharField(max_length=150,null=False,blank=False)
    meta_description = models.TextField(max_length=500,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class ProductModel(models.Model):
    category_forgn= models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    slug = models.CharField(max_length=120,null=False,blank=False)
    name = models.CharField(max_length=120,null=False,blank=False)
    product_image = models.ImageField(upload_to="image/",null=False,blank=False)
    description = models.TextField(max_length=500,null=True,blank=True)
    quantity = models.IntegerField(null=True,blank=True)
    price = models.IntegerField(null=False,blank=False)
    small_description = models.CharField(max_length=100,null=False,blank=False)
    status = models.BooleanField(default=False,help_text="0=defual,1=hidden")
    trending = models.BooleanField(default=False,help_text="1=defual,0=trending")
    # meta_title = models.CharField(max_length=140,null=False,blank=True)
    meta_keyword = models.CharField(max_length=150,null=False,blank=False)
    # meta_description = models.TextField(max_length=500,null=False,blank=False)
    # tag = models.CharField(max_length=120,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class User_Registration_Model(models.Model):
    User_Forgn=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    User_Contact=models.CharField(max_length=15)
    User_Address=models.CharField(max_length=100)
    User_Gender=models.CharField(max_length=10)
    User_Photo=models.ImageField(upload_to='image/')
    # status = models.BooleanField(default=False,help_text="0=defual,1=hidden")
    
    def __str__(self):
        return self.User_Forgn.first_name +" " + self.User_Forgn.last_name
    
class CartModel(models.Model):
    user_forgn = models.ForeignKey(User,on_delete=models.CASCADE)
    product_forgn = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    product_qty = models.IntegerField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class orderModel(models.Model):
    user_forgn = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100,null=False)
    address = models.CharField(max_length=250,null=False)
    state = models.CharField(max_length=50,null=False)
    city = models.CharField(max_length=50,null=False)
    number = models.IntegerField(null=False,blank=False)
    pincode = models.IntegerField(null=False,blank=False)
    email = models.EmailField(null=False)
    total_price = models.IntegerField(null=False,blank=False)
    payment_mode =models.CharField(max_length=100,null=False)
    payment_id = models.CharField(max_length=500,null=True,blank=True,default="1000000000000")
    orderstatus = (
        ('pending',"pending"),
        ("out for shipping","out for shipping"),
        ("completed","completed"),
    )
    status = models.CharField(max_length=200,choices=orderstatus,default="Out Of Delivary")
    message = models.CharField(max_length=200, null=True)
    tracking_no = models.CharField(max_length=200,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} - {}'.format(self.id,self.tracking_no)
    
class orderitemModel(models.Model):
    order_forgn = models.ForeignKey(orderModel,on_delete=models.CASCADE)
    product_forgn = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    price = models.IntegerField(null=False)
    quantity = models.IntegerField(null=True,blank=True)
    
    
    def __str__(self):
      return '{} - {}'.format(self.order_forgn.id,self.order_forgn.tracking_no)
    
    

