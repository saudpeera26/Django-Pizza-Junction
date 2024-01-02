from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from pizzaapp.models import pizza,Cart,Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import random
import razorpay

# Create your views here.
def home(request):
    username = request.user.username
    context={'username':username}
    return render(request,'home.html',context)


# -------------------------------------------------Menu page------------------------------------------------------------------


def menu(request):
    pizzadata=pizza.objects.all()
    username = request.user.username
    context={
        'pizzadata':pizzadata,
        'username':username
    }

    return render(request,'menu.html',context)


# -------------------------------------------------Cart logic/ add to cart & remove from cart------------------------------------------------------------------

def cart(req):
    if req.user.is_authenticated:
        username = req.user.username
        allcarts = Cart.objects.filter(userid=req.user.id)
        total_price = 0
        for x in allcarts:
            total_price += x.sno.pizza_price* x.qty
        length = len(allcarts)
        context = {
            "cart_items": allcarts,
            "total": total_price,
            "items": length,
            "username": username,
        }
        return render(req, "cart.html", context)
    else:
        allcarts = Cart.objects.filter(userid=req.user.id)
        total_price = 0
        for x in allcarts:
            total_price += x.sno.pizza_price * x.qty
        length = len(allcarts)
        context = {
            "cart_items": allcarts,
            "total": total_price,
            "items": length,
        }
        return render(req, "cart.html", context)
    


def add_to_cart(request, sno):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    pizzadata = get_object_or_404(pizza, sno=sno)
    cart_item, created = Cart.objects.get_or_create(sno=pizzadata, userid=user)
    if not created:
        cart_item.qty += 1
    else:
        cart_item.qty = 1
    cart_item.save()
    return redirect("/cart")

def remove_from_cart(request, sno):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    cart_item = Cart.objects.get(sno=sno, userid=user)
    cart_item.delete()
    return redirect("/cart")
# -------------------------------------------------Place order------------------------------------------------------------------

def remove_from_order(request, sno):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    orders=Order.objects.filter(userid=user,sno=sno)
    orders.delete()
    return redirect("/cart")

def updateqty(request, qv, sno):
    allcarts = Cart.objects.filter(sno=sno)
    if qv == "1":
        totol = allcarts[0].qty + 1
        allcarts.update(qty=totol)
    else:
        if allcarts[0].qty > 1:
            totol = allcarts[0].qty - 1
            allcarts.update(qty=totol)
        else:
            allcarts = Cart.objects.filter(sno=sno)
            allcarts.delete()

    return redirect("/cart")

def placeorder(request):
    if request.user.is_authenticated:
        user=request.user
    else:
        user=None
    allcarts = Cart.objects.filter(userid=user)
    total_price = 0
    length = len(allcarts)
    for x in allcarts:
        total_price += x.sno.pizza_price * x.qty
    context={}
    context['cart_items']=allcarts
    context['total']=total_price
    context['items']=length
    context['username']=user
    return render(request,'placeorder.html',context)

def showorders(req):
    if req.user.is_authenticated:
        user=req.user
        allorders = Order.objects.filter(userid=user)
        context = {"allorders": allorders, "username": user}
        return render(req, "orders.html", context)
    else:
        user=None
        return redirect('/userlogin')

# -------------------------------------------------Register-Login-logout------------------------------------------------------------------

def register(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        if uname == "" or upass == "" or ucpass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "register.html", context)
        elif ucpass != upass:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "register.html", context)
        else:
            try:
                u = User.objects.create(username=uname, password=upass)
                u.set_password(upass)
                u.save()
                return redirect("/userlogin")
            except Exception:
                context["errmsg"] = "User already exists"
                return render(req, "register.html", context)
    else:
        return render(req, "register.html")


def userlogin(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        upass = req.POST["upass"]
        context = {}
        if uname == "" and upass == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "login.html", context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(req, u)
                return redirect("/")
            else:
                context["errmsg"] = "Invalid username and password"
                return render(req, "login.html", context)
    else:
        return render(req, "login.html")
    


def userlogout(req):
    logout(req)
    return redirect("/")



def base(request):
    username = request.user.username
    context={'username':username}
    return render(request,'base.html',context)


# def makepayment(request):
#     return render (request,'payment.html')

# -------------------------------------------------Payment page------------------------------------------------------------------

def makepayment(request):
    if request.user.is_authenticated:
        user=request.user
        order_id=random.randrange(1000,9999)
        allcarts = Cart.objects.filter(userid=user)
        for x in allcarts:
            o=Order.objects.create(order_id=order_id,sno=x.sno,userid=x.userid,qty=x.qty)
            o.save()
            x.delete()
        orders=Order.objects.filter(userid=user)
        total_price = 0
        for x in orders:
            total_price += x.sno.pizza_price * x.qty
            oid=x.order_id
        client = razorpay.Client(auth=("rzp_test_gy6mN2EFNBQ5xd", "JIEKxoUVTACvAEgrOGuFbJax"))
        data = { "amount": total_price*100, "currency": "INR", "receipt": str(oid) }
        payment = client.order.create(data=data)
        # print(payment)
        context={}
        context['data']=payment
        context['amount']=payment
        return render(request,'payment.html',context)
    else:
        user=None
        return redirect('/userlogin')
    


def showorders(req):
    if req.user.is_authenticated:
        user=req.user
        allorders = Order.objects.filter(userid=user)
        context = {"allorders": allorders, "username": user}
        return render(req, "userorders.html", context)
    else:
        user=None
        return redirect('/userlogin')


def contact(request):
    return render(request,'contact-us.html')