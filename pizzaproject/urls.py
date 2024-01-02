"""
URL configuration for pizzaproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pizzaapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('menu/',views.menu,name='menu'),
    path('base/',views.base,name='base'),
    path('register/',views.register,name='register'),
    path('userlogin/',views.userlogin,name='userlogin'),
    path('cart/',views.cart,name='cart'),
    path('userlogout/',views.userlogout,name='userlogout'),
    path("add_to_cart/<int:sno>", views.add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<int:sno>',views.remove_from_cart,name='remove_from_cart'),
    path('remove_from_order/',views.remove_from_order,name='remove_from_order'),
    path("updateqty/<qv>/<sno>", views.updateqty, name="updateqty"),
    path('placeorder/',views.placeorder,name='placeorder'),
    path('makepayment/',views.makepayment,name='makepayment'),
    path('showorders/',views.showorders,name='showorders'),
    path('contact/',views.contact,name='contact'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
