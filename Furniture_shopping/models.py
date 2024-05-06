from django.db import models

# Create your models here.
class Login(models.Model):
    Username=models.CharField(max_length=100)
    Password=models.CharField(max_length=100)
    Type=models.CharField(max_length=50)

class Staff(models.Model):
    Name=models.CharField(max_length=50)
    Address=models.CharField(max_length=100)
    DOB=models.DateField()
    Phone=models.BigIntegerField()
    Email= models.CharField(max_length=100)
    Photo = models.CharField(max_length=100)
    Gender = models.CharField(max_length=100)
    Specialization = models.CharField(max_length=100)
    Experience = models.CharField(max_length=100)
    Status = models.CharField(max_length=100)
    LOGIN =models.ForeignKey(Login,on_delete=models.CASCADE)
class Category(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.CharField(max_length=100)

class Subcategory(models.Model):
    Name = models.CharField(max_length=100)
    Image = models.CharField(max_length=100)
    CATEGORY = models.ForeignKey(Category, on_delete=models.CASCADE,default="")

class Product(models.Model):
    SUBCATEGORY = models.ForeignKey(Subcategory, on_delete=models.CASCADE,default="")
    Product_Name=models.CharField(max_length=100)
    MRP=models.CharField(max_length=100)
    Offer_Price=models.CharField(max_length=100,default='')
    Colour=models.CharField(max_length=100)
    Description=models.CharField(max_length=100)
    Dimensions=models.CharField(max_length=100)
    Primary_Material=models.CharField(max_length=100)
    Room_Type=models.CharField(max_length=100)
    Image=models.CharField(max_length=100)
    Image1=models.CharField(max_length=100,default="")
    Image2=models.CharField(max_length=100,default="")


class Stock(models.Model):
    Quantity=models.CharField(max_length=100)
    PRODUCT =models.ForeignKey(Product,on_delete=models.CASCADE,default=1)
    date=models.DateField(default='11-02-2024')
#
class User(models.Model):
    Photo = models.CharField(max_length=50)
    UserName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone = models.BigIntegerField()
    Dob = models.DateField()
    Gender = models.CharField(max_length=100)
    Place = models.CharField(max_length=100)
    District = models.CharField(max_length=100)
    Pincode = models.CharField(max_length=100)
    Landmark = models.CharField(max_length=100)
    LOGIN =models.ForeignKey(Login,on_delete=models.CASCADE)

class Customization(models.Model):
    Product_Type = models.CharField(max_length=100)
    Room_Type = models.CharField(max_length=100)
    Colour = models.CharField(max_length=100)
    Material = models.CharField(max_length=100)
    Quantity = models.BigIntegerField()
    Description = models.CharField(max_length=100)
    Image = models.CharField(max_length=300)
    Status = models.CharField(max_length=100,default='')
    Date = models.DateField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE)

class Assignworks(models.Model):
    Status = models.CharField(max_length=100,default='')
    Date = models.DateField()
    Description = models.CharField(max_length=100)
    Startdate = models.DateField()
    Enddate = models.DateField()
    Duration = models.CharField(max_length=100)
    Priority = models.CharField(max_length=100)
    STAFF = models.ForeignKey(Staff, on_delete=models.CASCADE)
    CUSTOMIZATION = models.ForeignKey(Customization, on_delete=models.CASCADE)

class Cart(models.Model):
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    Quantity = models.CharField(max_length=100)


class Complaint(models.Model):
    Date = models.DateField()
    complaint =  models.CharField(max_length=1000)
    Reply = models.CharField(max_length=1000)
    Status = models.CharField(max_length=500)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)



class Ordermain(models.Model):
    Date = models.DateField()
    Amount = models.CharField(max_length=100)
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100,default='pending')


class Ordersub(models.Model):
    ORDER = models.ForeignKey(Ordermain, on_delete=models.CASCADE, default=1)
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    Quantity = models.CharField(max_length=100)

class Payment(models.Model):
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    ORDERSUB=models.ForeignKey(Ordersub,on_delete=models.CASCADE)
    date=models.DateField()
    status=models.CharField(max_length=30)



class Review(models.Model):
    review =  models.CharField(max_length=1000)
    rating = models.CharField(max_length=1000)
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    PRODUCT = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)



class Feedback(models.Model):
    feedback =  models.CharField(max_length=1000)
    Date = models.DateField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE, default=1)