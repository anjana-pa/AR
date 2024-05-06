import os
import smtplib
import string

from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from untitled.settings import MEDIA_ROOT
from  .models import *
# Create your views here.
def login(request):
    return  render(request,"loginindex.html")


def login_post(request):
    username=request.POST["textfield"]
    password=request.POST["textfield2"]
    if Login.objects.filter(Username=username,Password=password).exists():
        a=Login.objects.get(Username=username,Password=password)
        if a.Password == password:
            request.session['log'] = "lin"
            request.session['lid'] = a.id
            if a.Type=="Admin":
                return redirect('/Myapp/admin_home/')
            elif a.Type=="Staff":
                ff = Staff.objects.get(LOGIN_id=request.session['lid'])
                request.session['photo']=ff.Photo
                request.session['name']=ff.Name
                return HttpResponse('''<script>alert('Login Successful');window.location='/Myapp/staff_home/'</script>''')
            else:
                return HttpResponse("<script>alert('User not found');window.location='/Myapp/login/'</script>")
        else:
            return HttpResponse("<script>alert('User not found');window.location='/Myapp/login/'</script>")
    else:
        return HttpResponse("<script>alert('User not found');window.location='/Myapp/login/'</script>")


###############################################################################################################3


def StaffRegistration(request):
    if request.session['log'] =="lin":
        return  render(request,"Admin/staff registration.html")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def StaffRegistration_post(request):
    # if request.session['log'] == "lin":
        name=request.POST["textfield"]
        address=request.POST["textfield2"]
        dob=request.POST["textfield3"]
        phone=request.POST["textfield4"]
        email=request.POST["textfield5"]
        photo=request.FILES["fileField"]
        gender=request.POST["RadioGroup1"]
        Specialization=request.POST["select"]
        experience=request.POST["textfield6"]
        from datetime import datetime
        date=datetime.now().strftime('%Y%m%d-%H%M%S')+'.jpg'
        fs=FileSystemStorage()
        fs.save(date,photo)
        path=fs.url(date)
        b=Login()
        import random


        characters = string.ascii_letters + string.digits + string.punctuation


        new_pass = ''.join(random.choice(characters) for _ in range(8))
        b.Username=email
        b.Password=str(new_pass)
        b.Type='Staff'
        b.save()
        a=Staff()
        a.Name=name
        a.Address=address
        a.DOB=dob
        a.Phone=phone
        a.Email=email
        a.Photo=path
        a.Gender=gender
        a.Specialization=Specialization
        a.Experience=experience
        a.LOGIN_id=b.id
        a.save()
        return HttpResponse("<script>alert('Registered Successfully');window.location='/Myapp/ViewStaff/'</script>")

    # else:
    #     return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def EditStaff(request,id):
    if request.session['log'] == "lin":
        res=Staff.objects.get(id=id)
        return  render(request,"Admin/edit staff.html",{"data":res})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def EditStaff_post(request):
    if request.session['log'] == "lin":
        name=request.POST["textfield"]
        address=request.POST["textfield2"]
        dob=request.POST["textfield3"]
        phone=request.POST["textfield4"]
        email=request.POST["textfield5"]
        gender=request.POST["RadioGroup1"]
        Specialization=request.POST["select"]
        experience=request.POST["textfield7"]
        id=request.POST['id']

        if 'fileField' in request.FILES:
            photo = request.FILES["fileField"]
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, photo)
            path = fs.url(date)
            a = Staff.objects.get(id=id)
            a.Photo = path
            a.save()
        a = Staff.objects.get(id=id)
        a.Name = name
        a.Address = address
        a.DOB = dob
        a.Phone = phone
        a.Email = email

        a.Gender = gender
        a.Specialization = Specialization
        a.Experience = experience
        a.save()
        return HttpResponse("<script>alert('Update Successfully');window.location='/Myapp/ViewStaff/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def ViewStaff(request):
    if request.session['log'] == "lin":
        a=Staff.objects.all().order_by('-id')
        return render(request,"Admin/view staff.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewStaff_post(request):
    if request.session['log'] == "lin":
        search=request.POST["textfield"]
        a=Staff.objects.filter(Name__icontains=search)
        return render(request,"Admin/view staff.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def delete_staff(request,id):
    if request.session['log'] == "lin":
        # res=Staff.objects.filter(LOGIN__id=id).delete()

        res=Staff.objects.filter(LOGIN_id=id).update(Status='Block')
        ress=Login.objects.filter(id=id).update(Type='blocked')
        return HttpResponse("<script>alert('Blocked Successfully');window.location='/Myapp/ViewStaff/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def forgot_pass(request):
        return render(request, 'forgot.html')

def ForgotPassword_Post(request):
        Email = request.POST['textfield']
        if Login.objects.filter(Username=Email).exists():

            import random
            new_pass = random.randint(0000, 9999)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login("furnitures176@gmail.com", "ejqy qzsr qwwf ldbi")

            to = Email
            subject = "Test Email"
            body = "Your new password is " + str(new_pass)
            msg = f"Subject:{subject}\n\n{body}"
            server.sendmail("furnitures176@@gmail.com", to, msg)

            server.quit()
            Login.objects.filter(Username=Email).update(Password=new_pass)

            return HttpResponse("<script>alert('Please check your Email'); window.location='/Myapp/login/'</script>")
        return HttpResponse("<script>alert('No Email Found'); window.location='/Myapp/login/'</script>")


####################################################################################################################

def AddCategory(request):
    if request.session['log'] == "lin":
        return render(request,"Admin/Add category.html")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def AddCategory_post(request):
    if request.session['log'] == "lin":
        categoryname=request.POST["textfield"]
        image=request.FILES["fileField"]
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, image)
        path = fs.url(date)

        if Category.objects.filter(Name__icontains=categoryname).exists():
            return HttpResponse("<script>alert('Already exists');window.location='/Myapp/ViewCategory/'</script>")

        a = Category()
        a.Name = categoryname
        a.Image = path
        a.save()
        return HttpResponse("<script>alert('Successfully');window.location='/Myapp/ViewCategory/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def ViewCategory(request):
    if request.session['log'] == "lin":
        a = Category.objects.all().order_by('-id')
        return render(request, "Admin/view category.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewCategory_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Category.objects.filter(Name__icontains=search)
        return render(request, "Admin/view category.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def EditCategory(request,id):
    if request.session['log'] == "lin":
        res=Category.objects.get(id=id)
        return render(request,"Admin/Edit category.html",{"data":res})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def EditCategory_post(request):
    if request.session['log'] == "lin":
        pid=request.POST['pid']
        categoryname=request.POST["textfield"]

        if 'fileField' in request.FILES:
            image=request.FILES["fileField"]
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, image)
            path = fs.url(date)
            a = Category.objects.get(id=pid)
            a.Image = path
            a.save()

        a = Category.objects.get(id=pid)
        a.Name = categoryname
        a.save()
        return HttpResponse("<script>alert('Successfully');window.location='/Myapp/ViewCategory/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def delete_category(request,id):
    if request.session['log'] == "lin":
        res=Category.objects.filter(id=id).delete()
        return  HttpResponse("<script>alert('delete Successfully');window.location='/Myapp/ViewCategory/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")



def AddSubCategory(request,id):
    if request.session['log'] == "lin":
        return render(request, "Admin/AddSubCategory.html",{'id':id})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def AddSubCategory_post(request):
    if request.session['log'] == "lin":
        categoryname = request.POST["textfield"]
        id = request.POST["id"]
        image = request.FILES["fileField"]
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, image)
        path = fs.url(date)

        if Category.objects.filter(Name__icontains=categoryname).exists():
            return HttpResponse("<script>alert('Already Exists');window.location='/Myapp/ViewCategory/'</script>")

        a = Subcategory()
        a.Name = categoryname
        a.CATEGORY_id = id
        a.Image = path
        a.save()
        return HttpResponse("<script>alert('Successfully');window.location='/Myapp/ViewCategory/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewSubCategory(request,id):
    if request.session['log'] == "lin":
        a = Subcategory.objects.filter(CATEGORY_id=id).order_by('-id')
        return render(request, "Admin/ViewSubCategory.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewSubCategory_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Subcategory.objects.filter(Name__icontains=search)
        return render(request, "Admin/ViewSubCategory.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


###########################################################################################################

def admin_home(request):
    return render(request,'Admin/Adminindex.html')


def logout(request):
    return  render(request,"loginindex.html")

def staff_home(request):

    return render(request,'Staff/Staff_index1.html')




def admin_home(request):
    return render(request,'Admin/Adminindex12.html')


#########################################################################################################




def StaffViewCategory(request):
    if request.session['log'] == "lin":
        a = Category.objects.all().order_by('-id')
        return render(request, "Staff/SViewCategory.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def StaffViewCategory_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Category.objects.filter(Name__icontains=search)
        return render(request, "Staff/SViewCategory.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def StaffViewSubCategory(request,id):
    if request.session['log'] == "lin":
        a = Subcategory.objects.filter(CATEGORY_id=id).order_by('-id')
        return render(request, "Staff/SViewSubCategory.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def StaffViewSubCategory_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Subcategory.objects.filter(Name__icontains=search)
        return render(request, "Staff/SViewSubCategory.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def Add_Product(request):
    if request.session['log'] == "lin":
        ff = Staff.objects.get(LOGIN_id=request.session['lid'])
        a=Subcategory.objects.all()
        return render(request,"Staff/Add product.html",{'data':a,'data1':ff})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def Add_Product_post(request):
    if request.session['log'] == "lin":
        category =request.POST["select"]
        Product_Name=request.POST["Product_Name"]
        MRP = request.POST["MRP"]
        Offer_Price = request.POST["Offer_Price"]
        Colour = request.POST["Colour"]
        Description = request.POST["Description"]
        Primary_Material = request.POST["select2"]
        Room_Type = request.POST["select3"]
        Image=request.FILES["fileField"]
        Image1=request.FILES["fileField1"]
        Image2=request.FILES["fileField2"]
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
        fs = FileSystemStorage()
        fs.save(date, Image)
        path = fs.url(date)

        date1 = datetime.now().strftime('%Y%m%d-%H%M%S') + '1.jpg'
        fs1 = FileSystemStorage()
        fs1.save(date1, Image1)
        path1 = fs1.url(date1)

        date2 = datetime.now().strftime('%Y%m%d-%H%M%S') + '2.jpg'
        fs2 = FileSystemStorage()
        fs2.save(date2, Image2)
        path2 = fs2.url(date2)

        a=Product()
        a.SUBCATEGORY_id = category
        a.Product_Name = Product_Name
        a.MRP = MRP
        a.Offer_Price = Offer_Price
        a.Colour = Colour
        a.Description = Description
        a.Primary_Material = Primary_Material
        a.Room_Type = Room_Type
        a.Image = path
        a.Image1 = path1
        a.Image2 = path2
        a.save()

        return HttpResponse("<script>alert('Product Added Successfully');window.location='/Myapp/Add_Product/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def ViewProduct(request):
    if request.session['log'] == "lin":
        a=Product.objects.all().order_by('-id')
        return render(request,"Staff/View Product.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewProduct_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Product.objects.filter(Product_Name__icontains=search)
        return render(request, "Staff/View Product.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def EditProduct(request, id):
    if request.session['log'] == "lin":
        res = Product.objects.get(id=id)
        d=Subcategory.objects.all()
        return render(request, "Staff/Edit Product.html", {"data": res,'d':d})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def Edit_Product_post(request):
    if request.session['log'] == "lin":
        subcategory =request.POST["select"]
        Product_Name=request.POST["textfield"]
        MRP = request.POST["textfield2"]
        Offer_Price = request.POST["textfield3"]
        Colour = request.POST["textfield4"]
        Description = request.POST["textfield5"]
        Primary_Material = request.POST["select2"]
        Room_Type = request.POST["select3"]
        id = request.POST["id"]
        if 'fileField' in request.FILES:
            Image=request.FILES["fileField"]
            from datetime import datetime
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs = FileSystemStorage()
            fs.save(date, Image)
            path = fs.url(date)



            a=Product.objects.get(id=id)
            a.SUBCATEGORY_id=subcategory
            a.Product_Name=Product_Name
            a.MRP=MRP
            a.Offer_Price=Offer_Price
            a.Colour=Colour
            a.Description=Description
            a.Primary_Material=Primary_Material
            a.Room_Type=Room_Type
            a.Image=path

            a.save()

            return HttpResponse("<script>alert('Product Edit Successfully');window.location='/Myapp/ViewProduct/'</script>")
        elif 'fileField1' in request.FILES:
            Image1 = request.FILES["fileField1"]
            from datetime import datetime
            date1 = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs1 = FileSystemStorage()
            fs1.save(date1, Image1)
            path1 = fs1.url(date1)
            a = Product.objects.get(id=id)
            a.SUBCATEGORY_id = subcategory
            a.Product_Name = Product_Name
            a.MRP = MRP
            a.Offer_Price = Offer_Price
            a.Colour = Colour
            a.Description = Description
            a.Primary_Material = Primary_Material
            a.Room_Type = Room_Type
            a.Image1 = path1

            a.save()
            return HttpResponse("<script>alert('Product Edit Successfully');window.location='/Myapp/ViewProduct/'</script>")

        elif 'fileField2' in request.FILES:
            Image2 = request.FILES["fileField2"]
            from datetime import datetime
            date2 = datetime.now().strftime('%Y%m%d-%H%M%S') + '.jpg'
            fs2 = FileSystemStorage()
            fs2.save(date2, Image2)
            path2 = fs2.url(date2)
            a = Product.objects.get(id=id)
            a.SUBCATEGORY_id = subcategory
            a.Product_Name = Product_Name
            a.MRP = MRP
            a.Offer_Price = Offer_Price
            a.Colour = Colour
            a.Description = Description
            a.Primary_Material = Primary_Material
            a.Room_Type = Room_Type
            a.Image2 = path2

            a.save()
            return HttpResponse("<script>alert('Product Edit Successfully');window.location='/Myapp/ViewProduct/'</script>")


        else:
            a = Product.objects.get(id=id)
            a.SUBCATEGORY_id = subcategory
            a.Product_Name = Product_Name
            a.MRP = MRP
            a.Offer_Price = Offer_Price
            a.Colour = Colour
            a.Description = Description
            a.Primary_Material = Primary_Material
            a.Room_Type = Room_Type
            a.save()

            return HttpResponse(
                "<script>alert('Product Added Successfully');window.location='/Myapp/ViewProduct/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def delete_product(request,id):
    if request.session['log'] == "lin":
        res=Product.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('Ptoduct Delete Successfully');window.location='/Myapp/ViewProduct/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/login/'</script>")

################################################################################################


def Sstock(request):
    if request.session['log'] == "lin":
        ress=Product.objects.all()
        return render(request, "Staff/Stock.html",{'id':id,"data":ress})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/Stock/'</script>")


def Stock_post(request):
    if request.session['log'] == "lin":
        Quantity=request.POST['textfield']
        pid=request.POST['select3']
        rr=Stock.objects.filter(PRODUCT__id=pid)
        if rr.exists():
             t=int(Stock.objects.get(PRODUCT__id=pid).Quantity)+int(Quantity)
             a=Stock.objects.filter(PRODUCT__id=pid).update(Quantity=t)
        else:
            from datetime import datetime
            date=datetime.now()
            v=Stock()
            v.Quantity=Quantity
            v.date=date
            v.PRODUCT_id=pid
            v.save()

        return HttpResponse("<script>alert('Update Successfully');window.location='/Myapp/ViewStock/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/login/'</script>")


def ViewStock(request):
    if request.session['log'] == "lin":
        a=Stock.objects.all().order_by('-id')
        return render(request,"Staff/ViewStock.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewStock_post(request):
    if request.session['log'] == "lin":
        search=request.POST["textfield"]
        a=Product.objects.filter(Product_Name__icontains=search)
        return render(request,"Staff/ViewStock.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")



######################################################################################################

def ViewUser(request):
    if request.session['log'] == "lin":
        a=User.objects.all().order_by('-id')
        return render(request,"Admin/ViewUser.html",{'data':a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewUser_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = User.objects.filter(UserName__icontains=search)
        return render(request, "Admin/ViewUser.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

###################################################################################################


def ViewRequest(request):
    if request.session['log'] == "lin":
        a = Customization.objects.filter(Status='pending').order_by('-id')

        return render(request, "Admin/ViewRequest.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewRequest_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Customization.objects.filter(Product_Type__icontains=search,Status='pending')
        return render(request, "Admin/ViewRequest.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def accept_request(request, id):
    if request.session['log'] == "lin":
        res = Customization.objects.filter(id=id).update(Status='Approoved')
        return HttpResponse("<script>alert('Request Accepted Successfully');window.location='/Myapp/ViewRequest/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/login/'</script>")


def reject_request(request, id):
    if request.session['log'] == "lin":
        res = Customization.objects.filter(id=id).update(Status='Rejected')
        return HttpResponse( "<script>alert('Request Rejected Successfully');window.location='/Myapp/ViewRequest/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/login/'</script>")

def delete_request(request, id):
    if request.session['log'] == "lin":
        res = Customization.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('delete Successfully');window.location='/Myapp/ViewRequest/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


##############################################


def ViewAcceptedRequest(request):
    if request.session['log'] == "lin":
        a = Customization.objects.filter(Status='Approoved').order_by('-id')
        return render(request, "Admin/ViewAcceptedRequest.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewAcceptedRequest_post(request):
    if request.session['log'] == "lin":
        search = request.POST["select"]
        a = Customization.objects.filter(Product_Type__icontains=search)
        return render(request, "Admin/ViewAcceptedRequest.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def delete_acceptedrequest(request, id):
    if request.session['log'] == "lin":
        res = Customization.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('delete Successfully');window.location='/Myapp/ViewAcceptedRequest/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def get_available_trailers(request):
    asiigned_staff = Assignworks.objects.filter(~Q(Status="Completed")).values_list('id', flat=True)
    a = Staff.objects.exclude(id__in=asiigned_staff).values('id', 'Name').order_by('-id')

    return JsonResponse(list(a), safe=False)

def AssignWorks(request,id):
    if request.session['log'] == "lin":
        a=Staff.objects.all()
        c=Customization.objects.get(id=id)
        from datetime import datetime
        dt=datetime.now().today()
        return render(request, "Admin/AssignWorks.html", {'data': a,"data2":c,'dt':dt})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def AssignWorks_post(request):
    from datetime import datetime

    if request.session['log'] == "lin":
        st = request.POST['select']
        # Description = request.POST['textfield1']
        Priority = request.POST['select3']
        Startdate = datetime.strptime(request.POST['textfield3'], "%Y-%m-%d")  # Assuming date format is YYYY-MM-DD
        Enddate = datetime.strptime(request.POST['textfield4'], "%Y-%m-%d")  # Assuming date format is YYYY-MM-DD

        current_date = Startdate.today()

        if Startdate < current_date:
            return HttpResponse("<script>alert('Start date cannot be in the past');window.location='/Myapp/AssignWorks_post/'</script>")
        id = request.POST['id']
        date = datetime.now()

        # if Assignworks.objects.filter(STAFF_id=st, CUSTOMIZATION_id=id).exists():
        # r=Assignworks.objects.filter(Q STAFF_id=st || Q exclude(Status='Completed')
#         r=Assignworks.objects.filter(
#     Q(STAFF_id=st) | ~Q(Status='Completed')
# )
#         if r.exists():
#             return HttpResponse(
#                 "<script>alert('Already Exists');window.location='/Myapp/ViewAcceptedRequest/'</script>")

        v = Assignworks()
        nn=Customization.objects.filter(id=id).update(Status='assigned')
        v.STAFF_id = st
        v.CUSTOMIZATION_id = id
        v.Date = date
        v.Startdate = Startdate
        v.Enddate = Enddate
        duration = (Enddate - Startdate).days  # Calculate duration in days
        v.Duration = duration
        v.Priority = Priority
        # v.Description = Description
        v.Status = "pending"
        v.save()

        return HttpResponse("<script>alert('Assign Work Successfully');window.location='/Myapp/ViewRequest/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/login/'</script>")



def ViewWorks(request):
        if request.session['log'] == "lin":
            a = Assignworks.objects.filter(STAFF__LOGIN_id=request.session['lid']).order_by('-id')
            return render(request, "Staff/ViewWorks.html", {'data': a})
        else:
            return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

def ViewWorks_post(request):
        if request.session['log'] == "lin":
            search = request.POST["textfield"]
            a = Assignworks.objects.filter(CUSTOMIZATION__Product_Type__icontains=search, Status='pending')
            return render(request, "Staff/ViewWorks.html", {'data': a})
        else:
            return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


# def UpdateWorks(request):
#     if request.session['log'] == "lin":
#         a = Assignworks.objects.filter(STAFF__LOGIN_id=request.session['lid']).order_by('-id')
#         return render(request, "Staff/UpdateWork.html", {'data': a})
#     else:
#         return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")
#

def UpdateWorks(request,id):
    if request.session['log'] == "lin":
        a = Assignworks.objects.get(id=id)
        return render(request, "Staff/UpdateWork.html", {'i': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def UpdateWorks_post(request):
    id=request.POST['id']
    a = Assignworks.objects.get(id=id)
    sts=request.POST['select3']
    a.Status=sts
    a.save()
    return HttpResponse("<script>alert('Status Updated'); window.location='/Myapp/staff_home/'</script>")


def UpdateWork_post(request):
    if request.session['log'] == "lin":
        id=request.POST['id']
        res = Assignworks.objects.filter(id=id).update(Status='Completed')
        return HttpResponse("<script>alert('Status Update Successfully');window.location='/Myapp/ViewWorks/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/staff_home/'</script>")






def AdminViewComplaint(request):
    if request.session['log'] == "lin":
        a = Complaint.objects.all()
        return render(request, "Admin/ViewComplaint.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def AdminViewComplaint_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Complaint.objects.filter()
        return render(request, "Admin/ViewComplaint.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")






        ###########################################################################################################################################
                                               #USERRRRRRRRRRRRRRRRRRRRRRRRRRRR#
###########################################################################################################################################

def Login_post(request):
    uname = request.POST["uname"]
    password = request.POST["password"]
    lobj=Login.objects.filter(Username=uname,Password=password)
    if lobj.exists():
        a=Login.objects.get(Username=uname,Password=password)
        if a.Type=='user':
            lid=a.id
            b=User.objects.get(LOGIN_id=str(lid))
            name=b.UserName
            photo=b.Photo
            email=b.Email
            return JsonResponse({'status': 'ok','lid':str(lid),'name':name,'photo':photo,'email':email})
        else:
            return JsonResponse({'status': 'no'})


#####################################################################################################################################

def UserRegistration_post(request):

    Photo = request.POST["photo"]
    UserName = request.POST["uname"]
    Email = request.POST["email"]
    Phone = request.POST["phone"]
    Dob = request.POST["dob"]
    Gender = request.POST["gender"]
    Place = request.POST["place"]
    District = request.POST["district"]
    Pincode = request.POST["pincode"]
    Password = request.POST["password"]
    Landmark = request.POST["landmark"]
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    import base64
    a=base64.b64decode(Photo)
    fh=open("C:\\Users\\anjan\\PycharmProjects\\untitled\\media\\"+date+".jpg","wb")
    path = "/media/"+date+".jpg"
    fh.write(a)
    fh.close()
    l=Login()
    l.Username=Email
    l.Password=Password
    l.Type="user"
    l.save()

    a = User()
    a.Photo = path
    a.UserName = UserName
    a.Email = Email
    a.Phone = Phone
    a.Dob = Dob
    a.Gender = Gender
    a.Place = Place
    a.District = District
    a.Pincode = Pincode
    a.Landmark = Landmark
    a.LOGIN=l
    a.save()
    return JsonResponse({'status':'ok'})


def ViewProfile_post(request):
    lid = request.POST["lid"]
    print(lid,'llll')
    v=User.objects.get(LOGIN_id=lid)
    return JsonResponse({'status': 'ok','photo':v.Photo,'name':v.UserName,'email':v.Email,'phone':v.Phone,
                         'dob':v.Dob,'gender':v.Gender,'place':v.Place,'district':v.District,'pincode':v.Pincode,'landmark':v.Landmark})


def EditUser_post(request):
    lid = request.POST["lid"]
    Photo = request.POST["photo"]
    UserName = request.POST["name"]
    Email = request.POST["email"]
    Phone = request.POST["phone"]
    Dob = request.POST["dob"]
    Gender = request.POST["gender"]
    Place = request.POST["place"]
    District = request.POST["district"]
    Pincode = request.POST["pincode"]
    Landmark = request.POST["landmark"]
    aa = User.objects.get(LOGIN_id=lid)
    if len(Photo)<0:
        from datetime import datetime
        date = datetime.now().strftime('%Y%m%d-%H%M%S')
        import base64
        a = base64.b64decode(Photo)
        fh = open("C:\\Users\\anjan\\PycharmProjects\\untitled\\media\\" + date + ".jpg", "wb")
        path = "/media/" + date + ".jpg"
        fh.write(a)
        fh.close()
        aa.Photo=path
        aa.save()


    # if len(Photo)>0:
    # from datetime import datetime
    # # from encodings.base64_codec import base64_decode
    # # import base64
    # date = datetime.now().strftime('%Y%m%d-%H%M%S')
    #
    # import base64
    # # a = base64.b64decode(Photo)
    # # timestr = time.strftime("%Y%m%d-%H%M%S")
    # print(date)
    # b= base64.b64decode(Photo)
    # fh = open("C:\\Users\\anjan\\PycharmProjects\\untitled\\media\\user\\" + date + ".jpg", "wb")
    # path = "/media/user/" + date + ".jpg"
    # fh.write(b)
    # fh.close()

    aa.UserName = UserName
    aa.Email = Email
    aa.Phone = Phone
    aa.Dob = Dob
    aa.Gender = Gender
    aa.Place = Place
    aa.District = District
    aa.Pincode = Pincode
    aa.Landmark = Landmark
    aa.save()
    # else:
    #     aa.UserName = UserName
    #     aa.Email = Email
    #     aa.Phone = Phone
    #     aa.Dob = Dob
    #     aa.Gender = Gender
    #     aa.Place = Place
    #     aa.District = District
    #     aa.Pincode = Pincode
    #     aa.Landmark = Landmark
    return JsonResponse({'status':'ok'})



#######################################################################################################################################33

def UserViewCategory(request):
    res=Category.objects.all()
    l=[]
    for i in res:
        l.append({'id':i.id,'categoryname':i.Name,'image':i.Image})

    return JsonResponse({'status': 'ok','data':l})


def UserViewSubCategory(request):
    cat=request.POST['cid']
    res=Subcategory.objects.filter(CATEGORY_id=cat)
    l=[]
    for i in res:
        l.append({'id':i.id,'subcategoryname':i.Name,'image':i.Image})

    return JsonResponse({'status': 'ok','data':l})

def UserViewHomeCategory(request):
    res=Category.objects.all()
    l=[]
    for i in res:
        l.append({'id':i.id,'categoryname':i.Name})

    return JsonResponse({'status': 'ok','data':l})


def UserViewProduct(request):
    pid=request.POST['pid']

    res=Product.objects.filter(SUBCATEGORY=pid)
    l=[]
    for i in res:
        l.append({'id':i.id,'Product_Name':i.Product_Name,'MRP':i.MRP,'Offer_Price':i.Offer_Price,'Colour':i.Colour,'Description':i.Description,'Primary_Material':i.Primary_Material,'Room_Type':i.Room_Type,'Image':i.Image,'Image1':i.Image1,'Image2':i.Image2})
    print(l, 'pppppppppp')
    return JsonResponse({'status': 'ok','data':l})

def UserViewProductHome(request):
    res=Product.objects.filter()
    l=[]
    for i in res:
        l.append({'id':i.id,'Product_Name':i.Product_Name,'MRP':i.MRP,'Offer_Price':i.Offer_Price,'Colour':i.Colour,'Description':i.Description,'Primary_Material':i.Primary_Material,'Room_Type':i.Room_Type,'Image':i.Image,'Image1':i.Image1,'Image2':i.Image2})
    print(l, 'pppppppppp')
    return JsonResponse({'status': 'ok','data':l})



################################################################################################################################################3


def CustomizationRequest_post(request):
    lid = request.POST["lid"]
    Product_Type = request.POST["Product_Type"]
    Room_Type = request.POST["Room_Type"]
    # Size = request.POST["Size"]
    # Colour = request.POST["Colour"]
    Material = request.POST["Material"]
    # Spacing_Capacity = request.POST["Spacing_Capacity"]
    Quantity = request.POST["Quantity"]
    Description = request.POST["Description"]
    Image = request.POST["Image"]
    Date = request.POST["Date"]
    from datetime import datetime
    date = datetime.now().strftime('%Y%m%d-%H%M%S')
    import base64
    a = base64.b64decode(Image)
    # fh = open("C:\\Users\\anjan\\PycharmProjects\\untitled\\media\\" + date + ".jpg", "wb")
    fh = open("C:\\Users\\anjan\\PycharmProjects\\untitled\\media\\cust\\"+date+".jpg","wb")
    path = "/media/cust/"+ date +".jpg"
    fh.write(a)
    fh.close()



    a = Customization()
    a.Product_Type = Product_Type
    a.Room_Type = Room_Type
    # a.Size = Size
    # a.Colour = Colour
    a.Material = Material
    # a.Spacing_Capacity = Spacing_Capacity
    a.Quantity = Quantity
    a.Description = Description
    a.Image = path
    a.Date = Date
    a.Status = 'pending'
    a.USER=User.objects.get(LOGIN_id=lid)
    a.save()
    return JsonResponse({'status': 'ok'})



def ViewRequestStatus_post(request):
    lid = request.POST["lid"]
    print(lid,'llll')
    s=Customization.objects.all()
    l=[]
    for v in s:
        l.append({'Image':v.Image,'Product_Type':v.Product_Type,'Room_Type':v.Room_Type,'Material':v.Material,'Quantity':v.Quantity,'Description':v.Description,'Status':v.Status})
    return JsonResponse({'status': 'ok',"data":l})



def AddCart_post(request):
    lid = request.POST["lid"]
    pid = request.POST["pid"]
    Quantity = request.POST["Quantity"]
    print('login',lid)
    # print("dgvdubvhudbgkbvdhu "+lid)

    a = Cart()
    a.Quantity = Quantity
    a.PRODUCT = Product.objects.get(id=pid)
    a.USER = User.objects.get(LOGIN_id=lid)

    a.save()
    return JsonResponse({'status': 'ok'})


def user_viewcart(request):
    lid=request.POST['lid']
    res = Cart.objects.filter(USER__LOGIN_id=lid)
    l = []
    total=0
    for i in res:
        total+=(float(i.PRODUCT.Offer_Price)*int(i.Quantity))
        l.append({'id': i.id, 'Productname': i.PRODUCT.Product_Name,'MRP': i.PRODUCT.MRP,'Offerprice': i.PRODUCT.Offer_Price,'Colour':i.PRODUCT.Colour,'Quantity':i.Quantity,'Primarymaterial':i.PRODUCT.Primary_Material,'Roomtype':i.PRODUCT.Room_Type,'Image':i.PRODUCT.Image})
    print(l)
    print(total)
    return JsonResponse({'status': "ok", "data": l,"amount":int(total)})

def delete_cart(request):
    id=request.POST['id']
    a=Cart.objects.filter(id=id).delete()
    return JsonResponse({'status': 'ok'})




def user_makepayment(request):
    lid=request.POST['lid']

    # if Payment.objects.filter(Acname=Acname, Accn=Accn, Ifsc=Ifsc, Cvv=Cvv, Balance__gte=Amount).exists():
    mytotal = 0

    res2 = Cart.objects.filter(USER__LOGIN_id=lid)

    boj = Ordermain()
    boj.USER = User.objects.get(LOGIN_id=lid)

    boj.amount = 0
    import datetime
    boj.Date = datetime.datetime.now().today()
    boj.save()



    for j in res2:
        Quantity = int(j.Quantity)

        # stock = Stock.objects.filter(PRODUCT_id=j.PRODUCT_id, stock__gte=Quantity)
        # if stock.exists():
        print(j.PRODUCT.id,"hloooo")
        bs=Ordersub()
        bs.ORDER_id=boj.id
        bs.PRODUCT_id=j.PRODUCT.id
        bs.Quantity=j.Quantity
        bs.save()

        mytotal+=(float(j.PRODUCT.Offer_Price)*int(j.Quantity))

        print('hi')
        ab=Payment()
        ab.ORDERSUB = bs
        ab.date = datetime.datetime.now().today()
        ab.status = "completed"
        ab.USER = User.objects.get(LOGIN__id=lid)
        ab.save()

        resss=Ordermain.objects.filter(id=boj.id).update(status="paid",Amount=mytotal)

        mytotal+=(float(j.PRODUCT.Offer_Price)*int(j.Quantity))
        Cart.objects.filter(PRODUCT__id=j.PRODUCT.id).delete()



        f = Stock.objects.get(PRODUCT=j.PRODUCT)

        Stock.objects.filter(PRODUCT__id=j.PRODUCT.id).update(Quantity=int(f.Quantity) - int(j.Quantity))



    print(mytotal,"llllllllllllllllllll")

    Cart.objects.filter(USER__LOGIN_id=lid).delete()
    boj=Ordermain.objects.get(id=boj.id)
    boj.amount=mytotal
    boj.save()


    return JsonResponse({'k':'0','status':"ok"})
# else:
#

    #      return JsonResponse({"status":"no"})


def forgotpassword_post(request):
    email = request.POST['textfield']
    res = Login.objects.get(username=email)
    if res.exists():
        import random
        new_pass = random.randint(0000, 9999)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("s@gmail.com", "yqqlwlyqbfjtewam")  # App Password
        to = email
        subject = "Test Email"
        body = "Your new password is " + str(new_pass)
        msg = f"Subject: {subject}\n\n{body}"
        server.sendmail("s@gmail.com", to, msg)
        # Disconnect from the server        server.quit()
        ress = Login.objects.filter(username=email).filter(password=new_pass)
        return HttpResponse(  '''<script>alert('New password added.Please check your email..');window.location='/Myapp/login/'</script>''')
    else:
        return HttpResponse('''<script>alert('Invalid...');window.location='/Myapp/login/'</script>''')


def forgotpassword(request):
        return render(request, "loginindex.html")



def ViewOrderStatus_post(request):
    lid = request.POST["lid"]
    print(lid, 'llll')
    s = Ordersub.objects.filter(ORDER__USER__LOGIN_id=lid)
    l = []
    for v in s:
        l.append({'Image': v.PRODUCT.Image, 'Product_Name': v.PRODUCT.Product_Name,'Material': v.PRODUCT.Primary_Material,
                  'Quantity': v.Quantity,'Status': v.ORDER.status, 'Date': v.ORDER.Date,'Amount': v.ORDER.Amount})
        print(l)
    return JsonResponse({'status': 'ok', "data": l})

def user_change_password(request):
    lid = request.POST['lid']
    old_password = request.POST['old']
    new_password = request.POST['newp']
    c_password = request.POST['cp']
    res=Login.objects.filter(id=lid,Password=old_password)
    if res.exists():
        res1=Login.objects.get(id=lid,Password=old_password)
        if res1 is not None:
            if new_password==c_password:
                res1=Login.objects.filter(id=lid,Password=old_password).update(Password=c_password)
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'ok'})



def SendComplaint_post(request):
    lid = request.POST["lid"]
    pid = request.POST["pid"]
    from datetime import datetime
    Date=datetime.now().date().today()
    complaint = request.POST["complaint"]
    # reply = request.POST["reply"]

    a = Complaint()
    a.Date = Date
    a.complaint = complaint
    a.reply = 'pending'
    a.PRODUCT = Product.objects.get(id=pid)
    a.USER = User.objects.get(LOGIN_id=lid)

    a.save()
    return JsonResponse({'status': 'ok'})



def ViewReply_post(request):
    lid = request.POST["lid"]
    print(lid,'llll')
    s=Complaint.objects.filter(USER__LOGIN_id=lid).order_by('-id')
    l=[]
    for v in s:
        l.append({'id':v.id,'date':v.Date,'complaint':v.complaint,'reply':v.reply,'status':v.status})
    return JsonResponse({'status': 'ok',"data":l})




def sendcomplaintandviewstatus_POST(request):
    lid=request.POST['lid']
    pid=request.POST['pid']
    complaint=request.POST['complaint']
    # Status=['Pending']
    # Reply=['Pending']
    c=Complaint()
    c.complaint=complaint
    c.Status='Pending'
    c.Reply='Pending'
    from datetime import datetime
    c.Date=datetime.now().today()
    c.USER=User.objects.get(LOGIN_id=lid)
    c.PRODUCT_id=pid
    c.save()
    return JsonResponse({"status":"ok"})


def viewreply_POST(request):
    Lid = request.POST['lid']
    # a=Complaint.objects.filter(Student__LOGIN_id=Lid).order_by('-Date')USER__LOGIN_id=Lid
    a=Complaint.objects.filter()
    l=[]
    for i in a:
        l.append({'id':i.id,'complaint':i.complaint,'status':i.Status,'reply':i.Reply,'date':i.Date})
    return JsonResponse({"status":"ok",'data':l})

def viewcomplaint(request):
    if request.session['log'] == "lin":
        a = Complaint.objects.filter().order_by('-id')
        return render(request, 'Admin/AdminViewComplaint.html', {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def viewcomplaint_POST(request):
    if request.session['log'] == "lin":
        Fromdate = request.POST['textfield1']
        Todate = request.POST['textfield2']
        a = Complaint.objects.filter(Date__range=[Fromdate, Todate]).order_by('-id')
        return render(request, 'Admin/AdminViewComplaint.html', {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def sendreply(request, id):
    if request.session['log'] == "lin":
        return render(request, 'Admin/sendreply.html', {'id': id})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def sendreply_POST(request):
    if request.session['log'] == "lin":
        Reply = request.POST["textfield"]
        id = request.POST['id']
        Complaint.objects.filter(id=id).update(Reply=Reply, Status='Replied')
        return HttpResponse("<script>alert('Replayed'); window.location='/Myapp/viewcomplaint/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def staff_view_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "Staff/ViewProfile.html", {'data':ff})



def staff_edit_profile(request):
    ff=Staff.objects.get(LOGIN_id=request.session['lid'])
    return render(request, "Staff/ViewProfile.html/", {'data':ff})


def staff_edit_profile_post(request):
    Name = request.POST['Name']
    Address = request.POST['Address']
    DOB = request.POST['DOB']
    Phone = request.POST['Phone']
    Email = request.POST['Email']
    Photo = request.POST['Photo']
    Gender = request.POST['Gender']
    Specialization = request.POST['Specialization']
    Experience = request.POST['Experience']

    s = Staff.objects.get(LOGIN_id=request.session['lid'])

    if 'photo' in request.FILES:
        Photo = request.FILES['Photo']

        from datetime import datetime
        d = datetime.now().strftime('%Y%m%d_%H%M%S') + ".jpg"
        f = FileSystemStorage()
        f.save(d, Photo)
        path = f.url(d)
        s.photo = path
        s.save()
    else:
        s.Name = Name
        s.Address = Address
        s.DOB = DOB
        s.Phone = Phone
        s.Email = Email
        s.Photo = Photo
        s.Gender = Gender
        s.Specialization = Specialization
        s.Experience = Experience
        # s.photo = path
        s.save()
    # l = Login.objects.get(id=request.session['lid'])
    # l.username = email
    # l.password = password
    # l.save()

        return HttpResponse('''<script>alert("Profile Edited");window.location="/Myapp/staff_view_profile/"</script>''')


def Order_main(request):
    ab=Ordermain.objects.all().order_by('-id')
    print(ab)
    return render(request, 'Admin/OrderMain.html', {'data': ab})

def delete_ordermain(request,id):
    if request.session['log'] == "lin":
        res=Ordermain.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('Ptoduct Delete Successfully');window.location='/Myapp/Order_main/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out');window.location='/Myapp/login/'</script>")

def Order_sub(request,id):
    ab=Ordersub.objects.filter(ORDER__id=id)
    print(ab)
    return render(request, 'Admin/OrderSub.html', {'data': ab})



def staff_payment_status(request):
    nn=Ordersub.objects.all()
    print(nn)
    return render(request, 'Admin/PaymentStatus.html', {'data': nn})


def view_paymentstatus_search(request):
    search = request.POST['search']
    res = Payment.objects.filter()
    return render(request, 'Admin/PaymentStatus.html',{'data':res})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def generate_pdf(request, id):
    request.session['oid'] = id
    from fpdf import FPDF
    from datetime import datetime
    now = datetime.now().strftime('%B %d, %Y - %X')
    cst = Ordermain.objects.get(id=request.session['oid'])
    print(cst,"hloooo")
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Bill', 0, 1, 'C')
        def footer(self):
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Page %s' % self.page_no(), 0, 0, 'C')

        def add_bill_data(self, data):
            self.add_page()  # Add a page before adding content

            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Bill Details', ln=True, align='L')

            self.cell(0, 10, 'Bill Date: '+str(now), ln=True)
            self.cell(0, 10, 'Customer: '+cst.USER.UserName, ln=True)
            self.ln(10)  # Add space

            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Products', ln=True, align='L')

            # Add labels for product details
            self.cell(10, 10, '#', border=1)
            self.cell(50, 10, 'Product', border=1)
            self.cell(30, 10, 'Quantity', border=1)
            self.cell(30, 10, 'Price', border=1)
            self.cell(40, 10, 'Total', border=1)
            self.ln()

            for index, item in enumerate(data, start=1):
                self.cell(10, 10, str(index), border=1)
                self.cell(50, 10, item['product'], border=1)
                self.cell(30, 10, str(item['quantity']), border=1)
                self.cell(30, 10, f"Rs.{item['price']}", border=1)
                total = float(item['quantity']) * float(item['price'])
                self.cell(40, 10, f"Rs.{total}", border=1)
                self.ln()

            # Calculate total
            total = sum(float(item['quantity']) * float(item['price']) for item in data)
            self.cell(120, 10, 'Total:', border=1)
            self.cell(40, 10, f"Rs.{total}", border=1)

    bill_data = [
        {'product': i.PRODUCT.Product_Name, 'quantity': i.Quantity, 'price': i.PRODUCT.Offer_Price}
        for i in Ordersub.objects.filter(ORDER__id=request.session['oid'])
    ]
    print(request.session['oid'],"hlooooo")

    # Create PDF and add data
    pdf = PDF()
    pdf.add_bill_data(bill_data)


    pdf_filename = str(request.session['oid']) + 'bill.pdf'
    pdf.output(MEDIA_ROOT + '\\bills\\' + pdf_filename)
    response = HttpResponse(content_type='text/plain')
    pf = MEDIA_ROOT + '\\bills\\' + pdf_filename

    with open(pf, 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename={pdf_filename}'
    response.write('<script>window.location="/Myapp/Order_main/";</script>'.format('/Myapp/Order_main/'))
    # Order.objects.filter(id=request.session['oid']).update(status='Paid')
    return response
    # return redirect('/myapp/billing_view_bill/')


def ViewOrderMain_post(request):
    lid = request.POST["lid"]
    print(lid, 'llll')
    s = Ordermain.objects.filter(USER__LOGIN_id=lid).order_by('-Date')
    l = []
    for v in s:
        file = ''
        a='/media/bills/' + str(v.id)+"bill"+ '.pdf'
        l.append({'id':v.id,'Status': v.status, 'Date': v.Date,'Amount': v.Amount,"file":a})
        print(l)
        print(file,"kkkkkkk")
    return JsonResponse({'status': 'ok', "data": l})


#
# def user_view_order(request):
#     lid=request.POST['lid']
#     var=Order.objects.filter(USER__LOGIN_id=lid).order_by('-date')
#     l=[]
#     for i in var:
#         file = ''
#         try:
#             from SBS import settings
#             os.path.exists(settings.MEDIA_ROOT+'/bills/'+str(i.id)+'.pdf')
#             file = '/media/bills/'+str(i.id)+'bill.pdf'
#         except:
#             pass
#         l.append({'id':i.id,'date':i.date,'amount':i.amount,'status':i.security_status, 'file':file})
#
#     return JsonResponse({"status": "ok",'data':l})



def ViewOrderSub_post(request):
    lid = request.POST["lid"]
    oid = request.POST["oid"]
    print(lid, 'llll')
    s = Ordersub.objects.filter(ORDER__id=oid)
    l = []
    for v in s:
        l.append({'id':v.id,'pid': v.PRODUCT.id,'Name': v.PRODUCT.Product_Name, 'Image': v.PRODUCT.Image,'Quantity': v.Quantity})
        print(l)
    return JsonResponse({'status': 'ok', "data": l})


def ViewBill_post(request):
    lid = request.POST["lid"]
    oid = request.POST["oid"]
    print(lid, 'llll')
    s = Ordersub.objects.filter(ORDER__id=oid)
    l = []
    for v in s:
        l.append({'id':v.id,'Name': v.PRODUCT.Product_Name, 'Quantity': v.PRODUCT.Quantity,'Quantity': v.Quantity})
        print(l)
    return JsonResponse({'status': 'ok', "data": l})



def delete_payment(request, id):
    if request.session['log'] == "lin":
        res = Ordermain.objects.filter(id=id).delete()
        return HttpResponse("<script>alert('delete Successfully');window.location='/Myapp/OrderMain/'</script>")
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def View_single_product(request):
    pid = request.POST['pid']
    res = Product.objects.get(id=pid)

    res2=Stock.objects.get(PRODUCT_id=res)

    return JsonResponse({'status': 'ok','id': res.id,'stock':res2.Quantity, 'Product_Name': res.Product_Name, 'MRP': res.MRP, 'Offer_Price': res.Offer_Price,
             'Description': res.Description, 'Primary_Material': res.Primary_Material, 'Room_Type': res.Room_Type,
             'Image': res.Image, 'Image1': res.Image1, 'Image2': res.Image2})


def User_Review(request):
    lid = request.POST["lid"]
    pid = request.POST["pid"]
    rating = request.POST["rating"]
    review = request.POST["review"]


    a = Review()
    a.review = review
    a.rating = rating
    a.PRODUCT = Product.objects.get(id=pid)
    a.USER = User.objects.get(LOGIN_id=lid)

    a.save()
    return JsonResponse({'status': 'ok'})



def ViewReview(request):
    pid = request.POST["pid"]
    print(pid,'llll')
    s=Review.objects.filter(PRODUCT_id=pid)
    l=[]
    for v in s:
        l.append({'id':v.id,'review':v.review,'rating':v.rating})
        print(l)
    return JsonResponse({'status': 'ok',"data":l})



def Feedback_post(request):
    lid = request.POST["lid"]
    from datetime import datetime
    Date=datetime.now().date().today()
    feedback = request.POST["feedback"]
    # reply = request.POST["reply"]

    a = Feedback()
    a.Date = Date
    a.feedback = feedback
    a.USER = User.objects.get(LOGIN_id=lid)

    a.save()
    return JsonResponse({'status': 'ok'})



def AdminViewFeedback(request):
    if request.session['log'] == "lin":
        a = Feedback.objects.all()
        return render(request, "Admin/ViewFeedback.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")


def AdminViewFeedack_post(request):
    if request.session['log'] == "lin":
        search = request.POST["textfield"]
        a = Feedback.objects.filter()
        return render(request, "Staff/ViewFeedback.html", {'data': a})
    else:
        return HttpResponse("<script>alert('Your Loged Out'); window.location='/Myapp/login/'</script>")

