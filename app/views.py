from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from .models import *
import json
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
        user_login = "hidden"
        user_not_login = "show"
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    categories = Category.objects.filter(is_sub = False)
    context = {'form':form, 'user_login':user_login, 'user_not_login':user_not_login, 'categories':categories }
    return render(request,"app/register.html",context)

def loginPage(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
        return redirect('home')
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
        user_login = "hidden"
        user_not_login = "show"
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        user_by_username = User.objects.filter(username=username).first()
        if user is not None:
            login(request, user)
            return redirect('home')
        elif user_by_username is None: messages.info(request, 'Username chưa được đăng kí')
        else: messages.info(request, 'Nhập sai mật khâu')
    context = { 'user_login':user_login, 'user_not_login':user_not_login }
    return render(request,"app/login.html",context)

def logoutPage(request):
    logout(request)
    return redirect('home')


def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
        user_login = "hidden"
        user_not_login = "show"
        
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub = False)
    context = {'products' : products, 'cartItems':cartItems , 'user_login':user_login, 'user_not_login':user_not_login, 'categories':categories }
    return render(request,"app/home.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
        
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
        user_login = "hidden"
        user_not_login = "show"
        
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'user_login':user_login, 'user_not_login':user_not_login }
    return render(request,"app/cart.html",context)

def checkOut(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
        
    else:
        items= []
        cartItems = order['get_cart_items']
        order = {"get_cart_items":0,"get_cart_total":0 }
        user_login = "hidden"
        user_not_login = "show"
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'user_login':user_login, 'user_not_login':user_not_login }
    return render(request,"app/checkout.html",context)

def updateItem(request):
    data = json.loads(request.body)
    print(data)
    # Request body dc gui len server
    productId = data['productId']
    action = data['action']
    
    customer = request.user
    product = Product.objects.get(id = productId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order = order, product = product)
    
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("added",safe=False)

def searchProduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
        
    else:
        items= []
        cartItems = order['get_cart_items']
        order = {"get_cart_items":0,"get_cart_total":0 }
        user_login = "hidden"
        user_not_login = "show"
    if request.method == 'POST':
        searched = request.POST.get("searched", "").lower()  # Chuyển tất cả các ký tự sang chữ thường
        keys = Product.objects.filter(Q(name__icontains=searched) | Q(category__slug__icontains = searched))
        # Tìm kiếm cả theo tên sản phẩm và theo tên danh mục
    else:
        searched = ""
        keys = Product.objects.none()  # Trả về queryset rỗng nếu không có dữ liệu được gửi đi

    context = {'searched': searched, 'keys': keys,'items':items, 'order':order, 'cartItems':cartItems, 'user_login':user_login, 'user_not_login':user_not_login }
    return render(request, "app/search.html", context)

def categoryProduct(request):
    categories = Category.objects.filter(is_sub = False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categories, 'products':products, 'active_category':active_category}
    return render(request, "app/category.html", context)

def detailsProduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        user_login = "show"
        user_not_login = "hidden"
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
        user_login = "hidden"
        user_not_login = "show"
    id = request.GET.get('id', '')
    products = Product.objects.filter(id = id)
    categories = Category.objects.filter(is_sub = False)
    context = {'products' : products, 'cartItems':cartItems , 'user_login':user_login, 'user_not_login':user_not_login, 'categories':categories }
    return render(request, "app/product-details.html",context)