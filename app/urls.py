
from django.contrib import admin
from django.urls import path,include
from . import views 
urlpatterns = [
    path("",views.home, name="home"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkOut, name="checkout"),
    path("register/", views.register, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
    path("search/", views.searchProduct, name="search"),
    path("category/", views.categoryProduct, name="category"),
    path("details/", views.detailsProduct, name="details"),
    path("update_item/", views.updateItem, name="update_item")
]
