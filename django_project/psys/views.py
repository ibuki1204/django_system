from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from .forms import CustomerForm, CustomerUpdateForm
from django.contrib.auth.decorators import login_required




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
    customer = Customer.objects.get(customer_code=customer_code)

    if request.method == "POST":
        form = CustomerUpdateForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "得意先を更新しました")
            return redirect("customer_list")  # 追加：更新後は一覧へ戻すのが自然
        else:
            messages.error(request, "入力に誤りがあります")
    else:
        form = CustomerUpdateForm(instance=customer)

    return render(request, "psys/customer_update.html", {
        "form": form,
        "customer": customer,
    })

@login_required
def customer_delete(request, customer_code):
    customer = Customer.objects.get(customer_code=customer_code)
    customer.delete_flag = 1
    customer.save()
    messages.success(request, "得意先を削除しました")
    return redirect("customer_list")

