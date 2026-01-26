from django.shortcuts import render
from django.contrib import messages
from .models import Customer

def customer_search(request):
    keyword = request.GET.get("keyword", "")

    if keyword:
        customers = Customer.objects.filter(customer_name__contains=keyword)
    else:
        customers = Customer.objects.all()

    if not customers.exists():
        messages.error(request, "該当する得意先がありません")

    return render(request, "psys/customer_search.html", {
        "customers": customers,
        "keyword": keyword
    })

def index(request):
    return render(request, "psys/index.html")

def customer_list(request):
    customers = Customer.objects.all()
    if not customers.exists():
        messages.error(request, "得意先データがありません")
    return render(request, "psys/customer_list.html", {
        "customers": customers
    })