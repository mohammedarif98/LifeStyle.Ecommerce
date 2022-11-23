from xml.etree.ElementInclude import include
from App_lifestyle import views
from django.urls import path,include
from django.contrib.auth import views as auth_views




urlpatterns=[
    path("",views.Index,name="Index"),
    path('Admin_Home',views.Admin_Home,name='Admin_Home'),
    
    path("Registration_Page",views.Registration_Page,name="Registration_Page"),
    path('Registration',views.Registration,name='Registration'),
    path("Login_page",views.Login_page,name="Login_page"),
    path('User_Login',views.User_Login,name='User_Login'),
    path('User_Logout',views.User_Logout,name='User_Logout'),

    path("Mens",views.Mens,name='Mens'),
    path('Womens',views.Womens,name="Womens"),
    path('Accessories',views.Accessories,name="Accessories"),
    path("Product_Display/<int:pk>",views.Product_Display,name="Product_Display"),

#  user profile
    path('Profile_Page',views.Profile_Page,name='Profile_Page'),
    path('Profile_Edit_Page',views.Profile_Edit_Page,name="Profile_Edit_Page"),
    path('Profile_Edit',views.Profile_Edit,name="Profile_Edit"),
    
# cart 
    # path("add-to-cart",views.AddtoCart,name="AddtoCart"),
    path("Cart_View",views.Cart_View,name="Cart_View"),
    path('Add_Cart/<int:pk>',views.Add_Cart,name='Add_Cart'),
    path('Delete_Cart/<int:pk>',views.Delete_Cart,name='Delete_Cart'),
    
# booking
    path("placeorder",views.placeorder,name="placeorder"),
    path("proceed-to-pay",views.razorpay,name="proceed-to-pay"),
    
    path("orders",views.orders,name="orders"),
    path('orderview/<int:pk>',views.orderview,name="orderview"),
    
# invoice pdf   
    path("invoice/<int:pk>",views.invoice,name="invoice"),
    path("pdf_invoice/<int:pk>",views.pdf_invoice,name="pdf_invoice"),

# search
    path("search",views.search,name="search"),
    
# about and contact page
    path("About",views.About,name="About"),
    path("Contact",views.Contact,name="Contact"),
    path('Contact_Email',views.Contact_Email,name='Contact_Email'),
        
# facebook authentication
    path('oauth/', include('social_django.urls', namespace='social')),
    
# reset user passwords
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),   

]