from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse,HttpResponseRedirect
from .models import *
import json
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from random import sample
# Create your views here.
def register(request):
    if request.user.is_authenticated:
        customer = request.user
        
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
   
    context = {'form':form }
    return render(request,"app/register.html",context)

def loginPage(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
       
        return redirect('home')
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
       
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
    context = {}
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
       
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
       
    products = Product.objects.all().order_by("-date")
    
    # Lấy n sản phẩm ngẫu nhiên từ danh sách
    random_products = sample(list(products), ( len(products)))
    categories = Category.objects.all()
    context = {'products' : products,'categories' :categories, 'cartItems':cartItems, 'random_products': random_products   }
    return render(request,"app/home.html",context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items 
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
    categories = Category.objects.all()
    context = {'items':items, 'order':order, 'cartItems':cartItems, 'categories':categories}
    return render(request,"app/cart.html",context)

def checkOut(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        form = ShippingAddressForm()
        if request.method == 'POST':
            form = ShippingAddressForm(request.POST)
            if form.is_valid():
                form.instance.customer = customer
                form.instance.order = order
                form.save()
                for item in items:
                    product = item.product
                    quantity_to_reduce = item.quantity
                    if product.quantity >= quantity_to_reduce:
                        product.quantity -= quantity_to_reduce
                        product.save()
                        order.complete = True  # Đặt complete thành True
                        messages.info(request, f"Đã thanh toán thành công.")
                    else:
                        messages.info(request, f"Số lượng sản phẩm {product.name} chỉ còn {product.quantity}.")
                        order.complete = False
                order.save()  # Lưu lại đơn hàng sau khi complete đã được thay đổi
                return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        else:
            form = ShippingAddressForm()
    else:
        items= []
        cartItems = order['get_cart_items']
        order = {"get_cart_items":0,"get_cart_total":0 }
    
    categories = Category.objects.all()
    context = {'items':items, 'order':order,"form":form, 'cartItems':cartItems, "categories": categories}
    return render(request,"app/checkout.html",context)

def updateItem(request):
    data = json.loads(request.body)
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
    if action == 'delete':
        orderItem.delete()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse("added",safe=False)
def searchProduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items= []
        cartItems = order['get_cart_items']
        order = {"get_cart_items":0,"get_cart_total":0 }
       
    if request.method == 'POST':
        searched = request.POST.get("searched", "").lower()  
        keys = Product.objects.filter(Q(name__icontains=searched) | Q(category__slug__icontains = searched))
        
        # Tìm kiếm cả theo tên sản phẩm và theo tên danh mục
    else:
        searched = ""
        keys = Product.objects.none()  # Trả về queryset rỗng nếu không có dữ liệu được gửi đi
    categories = Category.objects.all()
    context = {'searched': searched, 'keys': keys,'items':items, 'order':order, 'cartItems':cartItems, "categories": categories }
    return render(request, "app/search.html", context)


def categoryProduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
       
        
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
       
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    categories = Category.objects.all()
    context = { 'products':products, 'active_category':active_category, "categories": categories,'items':items, 'order':order }
    
    return render(request, "app/category.html", context)

def detailsProduct(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer = customer, complete = False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
       
    else:
        items= []
        order = {"get_cart_items":0,"get_cart_total":0 }
        cartItems = order['get_cart_items']
       
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST, author = request.user, product = products)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    categories = Category.objects.all()
    context = {'products' : products,'form':form, 'cartItems':cartItems, "categories": categories   }
    return render(request, "app/product-details.html",context)

def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        try:
            profile_instance = request.user.profile
        except Profile.DoesNotExist:
            profile_instance = Profile.objects.create(user=request.user)

        p_form = ProfileUpdateForm(instance=profile_instance)
    
    categories = Category.objects.all()
        
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'categories':categories
    }

    return render(request, 'app/profile.html', context)
