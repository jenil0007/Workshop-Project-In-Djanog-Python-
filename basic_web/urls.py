"""
URL configuration for basic_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views. Home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from myApp import views
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.user_login, name='userLogin'),
    path('register/', views.user_register, name='user_register'),
    path('profile/', views.profile, name='profile'),
    path('Home/', views.home_page, name='homePage'),
    path('Home/payment/', views.payment, name='payment'),
    path('logout/', views.logout_view, name='logout'),
    path('Home/payment/payment-handler/', views.paymenthandler, name='payment_handler'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
