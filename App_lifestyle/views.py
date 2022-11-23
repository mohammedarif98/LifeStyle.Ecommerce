from email import message
import email
from http import client
from multiprocessing import context
from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User,auth
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from App_lifestyle.forms import *
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
import random
from django.template.loader import get_template
from xhtml2pdf import pisa



# ------------ home page ----------------

# @login_required(login_url='/')
def Index(request): 
    # if request.user.is_authenticated:
        mtrending = ProductModel.objects.filter(trending=0,category_forgn__name="Mens")
        wtrending = ProductModel.objects.filter(trending=0,category_forgn__name="Womens")
        context = {"mtrending":mtrending,'wtrending':wtrending}
        return render(request,"user/index.html",context)
    # return redirect('Index')

def Mens(request):
    product = ProductModel.objects.filter(category_forgn__name="Mens",status=0,)
    paginator = Paginator(product,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"product":page_obj,}
    return render(request,"user/mensproduct.html",context)

def Womens(request):
    product = ProductModel.objects.filter(category_forgn__name="Womens",status=0)
    paginator = Paginator(product,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"product":page_obj,}
    return render(request,"user/womensproduct.html",context)

def Accessories(request):
    product = ProductModel.objects.filter(category_forgn__name="Accessories",status=0)
    paginator = Paginator(product,8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"product":page_obj,}
    return render(request,"user/accessoriesproduct.html",context)

def Product_Display(request,pk):
    product_view = ProductModel.objects.get(id=pk)
    context = {"product_view":product_view}
    return render(request,"user/displayproduct.html",context)

# ---------- Admin Home --------------

def Admin_Home(request):
    if not request.user.is_staff:
        return redirect('Login_page')
    return render(request,'admin/admin_home.html')

# -------------- user login,signup and logout  -------------------

def Registration_Page(request):
    return render(request,"user/signup.html")

def Registration(request):
    if request.method=='POST':
        fname=request.POST['firstname']
        lname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        gender=request.POST['gender']
        password=request.POST['password']
        confirm_password=request.POST['c_password']
        address=request.POST['address']
        contact=request.POST['contact']
        if request.FILES.get('photo') is not None:
            photo = request.FILES.get('photo')
        else:
            photo = "static/images/userimage.png"
        # photo=request.FILES.get('photo')

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.info(request,"this username is already exist !")
                return redirect("Registration_Page")
        
            elif User.objects.filter(email = email).exists():
                messages.info(request,"this email is already exist !")
                return redirect("Registration_Page")

            else:
                user=User.objects.create_user(username=username,first_name=fname,last_name=lname,email=email,password=password)
                my_dict={'username':username}
                user.save() 

                # email message==============
                html_template = 'user/emil-temp.html'
                html_msg = render_to_string (html_template,context=my_dict)
                subject = "welcome you are successfully registered"
                email_form = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message= EmailMessage(subject,html_msg,email_form,recipient_list)
                message.content_subtype='html'
                message.send()

                messages.success(request,"Successfully Registered")

                user_data = User.objects.get(id=user.id)
                extented_user_data=User_Registration_Model(User_Gender=gender,User_Photo=photo,User_Address=address,User_Contact=contact,User_Forgn=user_data)
                extented_user_data.save()
                messages.success(request, 'SuccessFully Registered')
                print('success')
                return redirect('Login_page')
        
        else:
            messages.warning(request,"password not matching")
            print("password not matching....")
            return redirect('Registration_Page')
    else:
        return redirect('Registration_Page')

def Login_page(request):
    return render(request,"user/login.html")

def User_Login(request):
    if request.user.is_authenticated:
        return redirect(Index)
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        
        if user is not None:
            if user.is_staff:
                login(request,user)
                messages.info(request,f"You are now logged in as {username}")
                return redirect('Admin_Home')
                print("admin logged")
                
            else:
                login(request,user)
                auth.login(request,user)
                messages.info(request,f'welocome {username}')
                return redirect('Index')
        else: 
            messages.warning(request,"Username or Password is incorrect")
            return redirect('User_Login')
    else:
        return redirect('Admin_Home')  # "admin_home"

def User_Logout(request):
    # request.session['uid']=""             # session id method
    if request.user.is_authenticated:     # is authenticated method
        auth.logout(request)
    return redirect('Index')

# -------------- user profile ---------------

@login_required(login_url='Login_page')
def Profile_Page(request):
    user_data=User_Registration_Model.objects.get(User_Forgn=request.user)
    context={'users':user_data}
    return render(request,'user/profile.html',context)

@login_required(login_url='Login_page')
def Profile_Edit_Page(request):
    user_data=User_Registration_Model.objects.get(User_Forgn=request.user)
    context={'edit_data':user_data}
    return render(request,'user/edit_profile.html',context)

@login_required(login_url='Login_page')
def Profile_Edit(request):
    if request.method=='POST':
        user_data=User_Registration_Model.objects.get(User_Forgn=request.user)
        user_data.User_Forgn.first_name=request.POST['firstname']
        user_data.User_Forgn.last_name=request.POST['lastname']
        user_data.User_Forgn.username=request.POST['username']
        user_data.User_Forgn.email=request.POST['email']
        user_data.User_Gender=request.POST['gender']
        user_data.User_Address=request.POST['address']
        user_data.User_Contact=request.POST['contact']
        # user_data.User_Photo = request.FILES['photo']
        if request.FILES.get('photo') is not None:
            user_data.User_Photo= request.FILES.get('photo')

        user_data.save()
        user_data.User_Forgn.save()
        return redirect('Profile_Page')

# ------------- contact and about-us page --------------

def About(request):
    return render(request,'user/about.html')

def Contact(request):
    return render(request,'user/contact.html')

def Contact_Email(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        message=request.POST.get('message')

    data={'name':name,'email':email,'message':message}
    message= '''
    new massage : {}
    from : {}
    '''.format(data['message'],data['email'],)
    send_mail(data['name'],message,'',['bookmyrooms2021@gmail.com'])
    return render(request,'user/contact.html')


'''----------- cart --------------'''
@login_required(login_url='Login_page')
def Cart_View(request):
    products=CartModel.objects.filter(user_forgn=request.user)
    sum=100
    for i in products:
        sum+=i.product_forgn.price
    
    count=products.count()
    
    context={'products':products,'sum':sum,'count':count}
    return render(request,'user/cart.html',context)

@login_required(login_url='Login_page')
def Add_Cart(request,pk):
    product = ProductModel.objects.get(id=pk)
    # user = adduser_model.objects.get(user=request.user)
    data = CartModel(product_forgn=product,user_forgn=request.user)
    messages.info(request,"item added to cart")
    data.save()
    return redirect('Cart_View')

@login_required(login_url='Login_page')
def Delete_Cart(request,pk):
    cart=CartModel.objects.get(id=pk)
    messages.info(request,"item removed to cart")
    cart.delete()
    return redirect('Cart_View')


'''=========== checkout =============='''
@login_required(login_url='Login_page')
def placeorder(request):
        if request.method=='POST':
            neworder=orderModel()
            neworder.user_forgn=request.user
            neworder.name=request.POST['name']
            neworder.number=request.POST['number']
            neworder.email=request.POST['email']
            neworder.pincode=request.POST['pincode']
            neworder.state=request.POST['state']
            neworder.city=request.POST['city']
            neworder.address=request.POST['address']
            
            neworder.payment_id = request.POST.get('payment_id')
            neworder.payment_mode = request.POST['payment_mode']
            
            cart = CartModel.objects.filter(user_forgn=request.user)
            cart_total_price = 100
            for item in cart:
                cart_total_price = cart_total_price + item.product_forgn.price
                
            neworder.total_price = cart_total_price
            
            trackno = 'lisfestyle'+str(random.randint(11111111,999999999))
            while orderModel.objects.filter(tracking_no=trackno) is None:
                trackno = 'lifestyle'+str(random.randint(11111111,999999999))
                
            neworder.tracking_no = trackno
            neworder.save()
            
            neworderitem = CartModel.objects.filter(user_forgn=request.user)
            for item in neworderitem:
                orderitemModel.objects.create(
                    order_forgn = neworder,
                    product_forgn = item.product_forgn,
                    price = item.product_forgn.price,
                    # quantity = item.product_qty
                )
            
            cart = CartModel.objects.filter(user_forgn=request.user).delete()
            
    
            
            paymode = request.POST.get('payment_id')
            if (paymode == "paid by razorpay"):
                return JsonResponse({'status':"your order has been placed successfully"})
            else:
                messages.success(request,'your order placed successfully')   
                
            return redirect('Cart_View')  
    
@login_required(login_url='Login_page')
def razorpay(request):
        cart=CartModel.objects.filter(user_forgn=request.user)
        total_price=0
        for item in cart:
            total_price=total_price+item.product_forgn.price+100
            
        return JsonResponse({
            'total_price':total_price
        })
        
        
# @login_required(login_url='Login_page')
def orders(request):
    order  = orderModel.objects.filter(user_forgn=request.user)
    context = {'order':order}
    return render(request,'user/order.html',context)
    # return HttpResponse("my order page")

def orderview(request,pk):
    order = orderModel.objects.filter(id=pk).filter(user_forgn=request.user).first()
    orderitem = orderitemModel.objects.filter(order_forgn=order)
    context = {'order':order,'orderitem':orderitem}
    return render(request,'user/orderview.html',context)


''' ---------- invoice pdf creation ------------ '''

def invoice(request,pk):
    orders = orderModel.objects.filter(id=pk).filter(user_forgn=request.user).first()
    order = orderitemModel.objects.filter(order_forgn=orders)
    # order = orderitemModel.objects.filter(id=pk).filter(order_forgn__user_forgn=request.user)
    return render(request,"user/invoicelist.html",context={'order':order,'orders':orders})

def pdf_invoice(request,pk):
    orders = orderModel.objects.filter(id=pk).filter(user_forgn=request.user).first()
    order = orderitemModel.objects.filter(order_forgn=orders)
    template_path = 'user/product_invoice.html'
    context = {'order':order,'orders':orders}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="ProductInvoice.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


'''-----------  search function --------------'''

def search(request):
    # if request.method == "GET":
        query = request.GET.get('query')
        prod = ProductModel.objects.filter(slug__icontains=query)
        paginator = Paginator(prod,8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context={"product":page_obj,}
        return render(request,"user/search.html",context)

        # print("no result")
        # return request(request,'user/Index.html')
    # return HttpResponse("this is seacrch")







     


