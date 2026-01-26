# psys/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),

    # メニュー
    path("main_menu/", views.main_menu, name="main_menu"),
    path("customer_management_menu/", views.customer_management_menu, name="customer_management_menu"),

    # 得意先
    path("customer/list/", views.customer_list, name="customer_list"),
    path("customer/regist/", views.customer_regist, name="customer_regist"),
    path("customer/search/", views.customer_search, name="customer_search"),

    path("customer/update/select/", views.customer_update_select, name="customer_update_select"),
    path("customer/update/<str:customer_code>/", views.customer_update, name="customer_update"),
    path("customer/update/<str:customer_code>/result/", views.customer_update_result, name="customer_update_result"),

    path("customer/delete/select/", views.customer_delete_select, name="customer_delete_select"),
    path("customer/delete/<str:customer_code>/", views.customer_delete, name="customer_delete"),
    path("customer/delete/<str:customer_code>/result/", views.customer_delete_result, name="customer_delete_result"),

    path("customer/summary/", views.customer_summary, name="customer_summary"),

    path("customer/summary/detail/<str:customer_code>/", views.customer_summary_detail, name="customer_summary_detail"),

    path("orders/<str:order_no>/details/", views.order_details, name="order_details"),




]



