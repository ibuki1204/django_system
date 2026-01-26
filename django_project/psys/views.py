from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm, CustomerUpdateForm


@login_required
def main_menu(request):
    return render(request, "psys/main_menu.html")

@login_required
def customer_management_menu(request):
    return render(request, "psys/customer_management_menu.html")

def index(request):
    return render(request, "psys/index.html")

@login_required
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

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    if not customers.exists():
        messages.error(request, "得意先データがありません")
    return render(request, "psys/customer_list.html", {
        "customers": customers
    })

@login_required
def customer_regist(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "得意先を登録しました")
            form = CustomerForm()  # 入力欄を空にする
        else:
            messages.error(request, "入力に誤りがあります")
    else:
        form = CustomerForm()

    return render(request, "psys/customer_regist.html", {"form": form})


# ★ ここから customer_id → customer_code に変更
@login_required
def customer_update(request, customer_code):
    customer = get_object_or_404(Customer, customer_code=customer_code)

    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect("customer_update_result", customer_code=customer.customer_code)
        messages.error(request, "入力に誤りがあります")
    else:
        form = CustomerUpdateForm(instance=customer)

    return render(request, "psys/customer_update.html", {
        "form": form,
        "customer": customer,
    })


@login_required
def customer_update_result(request, customer_code):
    customer = get_object_or_404(Customer, customer_code=customer_code)
    return render(request, "psys/customer_update_result.html", {"customer": customer})


@login_required
def customer_delete(request, customer_code):
    customer = get_object_or_404(Customer, customer_code=customer_code)

    if request.method == "POST":
        customer.delete_flag = 1
        customer.save()
        return redirect("customer_delete_result", customer_code=customer_code)

    # GETは確認画面
    return render(request, "psys/customer_delete.html", {"customer": customer})


@login_required
def customer_delete_result(request, customer_code):
    return render(request, "psys/customer_delete_result.html", {"customer_code": customer_code})

