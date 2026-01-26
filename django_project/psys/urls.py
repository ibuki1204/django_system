from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("customer/search/", views.customer_search, name="customer_search"),
    path("customer/list/", views.customer_list, name="customer_list"),
    path("customer/regist/", views.customer_regist, name="customer_regist"),

]

