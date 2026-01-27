from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Customer, Orders, OrderDetails
from .forms import CustomerForm, CustomerUpdateForm
from django.db.models import Sum, Count
from .models import Employee
from django.contrib.auth.models import User
from django.db import transaction



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
        customers = Customer.objects.filter(delete_flag=0, customer_name__contains=keyword)
    else:
        customers = Customer.objects.filter(delete_flag=0)

    if not customers.exists():
        messages.error(request, "該当する得意先がありません")

    return render(request, "psys/customer_search.html", {
        "customers": customers,
        "keyword": keyword
    })


@login_required
def customer_list(request):
    customers = Customer.objects.filter(delete_flag=0)
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
            customer = form.save(commit=False)
            customer.delete_flag = 0
            customer.save()
            messages.success(request, "得意先を登録しました")
            return redirect("customer_list")
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

    # 追加：ログインユーザーの従業員情報をemployeeテーブルから取得（失敗しても落とさない）
    employee = None
    try:
        employee = Employee.objects.get(employee_no=request.user.username)
    except Exception:
        employee = None

    if request.method == "POST":
        customer.delete_flag = 1
        customer.save()
        return redirect("customer_delete_result", customer_code=customer_code)

    return render(request, "psys/customer_delete.html", {
        "customer": customer,
        "employee": employee,  # 追加
    })


@login_required
def customer_delete_result(request, customer_code):
    return render(request, "psys/customer_delete_result.html", {"customer_code": customer_code})

@login_required
def customer_summary(request):
    date_from = request.GET.get("from", "")
    date_to = request.GET.get("to", "")

    orders_qs = Orders.objects.all()

    # 期間指定（任意）
    if date_from:
        orders_qs = orders_qs.filter(order_date__gte=date_from)
    if date_to:
        orders_qs = orders_qs.filter(order_date__lte=date_to)

    summary = (
        orders_qs.values(
            "customer_code__customer_code",
            "customer_code__customer_name",
        )
        .annotate(
            order_count=Count("order_no"),
            total_amount=Sum("total_price"),
        )
        .order_by("customer_code__customer_code")
    )

    return render(request, "psys/customer_summary.html", {
        "summary": summary,
        "date_from": date_from,
        "date_to": date_to,
    })

@login_required
def customer_summary_detail(request, customer_code):
    date_from = request.GET.get("from", "")
    date_to = request.GET.get("to", "")

    customer = get_object_or_404(Customer, customer_code=customer_code)

    orders_qs = Orders.objects.filter(customer_code=customer)

    # 期間指定（集計画面から引き継ぐ）
    if date_from:
        orders_qs = orders_qs.filter(order_date__gte=date_from)
    if date_to:
        orders_qs = orders_qs.filter(order_date__lte=date_to)

    orders_qs = orders_qs.order_by("-order_date", "-order_no")

    return render(request, "psys/customer_summary_detail.html", {
        "customer": customer,
        "orders": orders_qs,
        "date_from": date_from,
        "date_to": date_to,
    })

@login_required
def order_details(request, order_no):
    order = get_object_or_404(Orders, order_no=order_no)

    details = (
        OrderDetails.objects
        .filter(order_no=order)          # FKならこれでOK
        .select_related("item_code")     # item_code がFKなら商品名も取れる
        .order_by("item_code")
    )

    total_detail = details.aggregate(s=Sum("order_price"))["s"] or 0

    return render(request, "psys/order_details.html", {
        "order": order,
        "details": details,
        "total_detail": total_detail,
    })

@login_required
def customer_update_select(request):
    customer = None
    customer_code = ""

    if request.method == "POST":
        customer_code = request.POST.get("customer_code", "").strip()
        if customer_code:
            customer = Customer.objects.filter(delete_flag=0, customer_code=customer_code).first()
            if customer:
                # 見つかったら更新画面へ
                return redirect("customer_update", customer_code=customer.customer_code)
            messages.error(request, "該当する得意先がありません")
        else:
            messages.error(request, "得意先コードを入力してください")

    return render(request, "psys/customer_update_select.html", {
        "customer_code": customer_code,
        "customer": customer,
    })


@login_required
def customer_delete_select(request):
    customer = None
    customer_code = ""

    if request.method == "POST":
        customer_code = request.POST.get("customer_code", "").strip()
        if customer_code:
            customer = Customer.objects.filter(delete_flag=0, customer_code=customer_code).first()
            if customer:
                # 見つかったら削除確認画面へ
                return redirect("customer_delete", customer_code=customer.customer_code)
            messages.error(request, "該当する得意先がありません")
        else:
            messages.error(request, "得意先コードを入力してください")

    return render(request, "psys/customer_delete_select.html", {
        "customer_code": customer_code,
        "customer": customer,
    })


def signup(request):
    if request.method == "POST":
        employee_no = request.POST.get("employee_no", "").strip()
        employee_name = request.POST.get("employee_name", "").strip()
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        # 入力チェック
        if not employee_no or not employee_name or not password1 or not password2:
            messages.error(request, "未入力の項目があります。")
            return render(request, "psys/signup.html")

        if len(employee_no) != 6:
            messages.error(request, "従業員番号は6桁で入力してください。")
            return render(request, "psys/signup.html")

        if password1 != password2:
            messages.error(request, "パスワードが一致しません。")
            return render(request, "psys/signup.html")

        if User.objects.filter(username=employee_no).exists():
            messages.error(request, "この従業員番号は既に登録されています。")
            return render(request, "psys/signup.html")

        if Employee.objects.filter(employee_no=employee_no).exists():
            messages.error(request, "employeeテーブルに同じ従業員番号が既に存在します。")
            return render(request, "psys/signup.html")

        # 👇 正しい try-except + transaction.atomic の構造
        try:
            with transaction.atomic():
                # User作成
                User.objects.create_user(
                    username=employee_no,
                    password=password1,
                    first_name=employee_name,
                )

                # Employee作成
                emp = Employee(
                    employee_no=employee_no,
                    employee_name=employee_name,
                )
                emp.save()

        except Exception as e:
            messages.error(request, f"登録に失敗しました：{e}")
            return render(request, "psys/signup.html")

        messages.success(request, "新規登録が完了しました。ログインしてください。")
        return redirect("login")

    return render(request, "psys/signup.html")
