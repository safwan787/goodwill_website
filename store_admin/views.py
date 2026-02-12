from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from .models import Category
from .forms import CategoryForm
from .models import Order, OrderItem
from django.shortcuts import render, get_object_or_404, redirect


def admin_login(request):
    """
    Custom login page.
    Uses Django username & password.
    Does NOT depend on Django admin login.
    """

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)   # creates session HERE
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'gd_admin/login.html')


@login_required
def admin_dashboard(request):
    return render(request, "gd_admin/dashboard.html", {
        "active": "dashboard"
    })



def admin_logout(request):
    logout(request)
    return redirect('admin_login')

# views.py
# store_admin/views.py
from django.contrib.auth.models import User
from .models import Product, Category, Order

from django.contrib.auth.models import User
from .models import Product, Category, Order
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):
    product_count = Product.objects.count()
    category_count = Category.objects.count()
    order_count = Order.objects.count()
    admin_count = User.objects.filter(is_staff=True).count()

    return render(request, "gd_admin/dashboard.html", {
        "product_count": product_count,
        "category_count": category_count,
        "order_count": order_count,
        "admin_count": admin_count,
        "active": "dashboard",
    })



def admin_product_list(request):
    products = Product.objects.select_related("category").all()

    return render(request, "gd_admin/product_list.html", {
        "products": products,
        "active": "products"
    })

def admin_product_add(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            messages.success(request, "Product added successfully")  # ✅ HERE

            return redirect("admin_products")
    else:
        form = ProductForm()

    return render(request, "gd_admin/product_form.html", {
        "form": form,
        "title": "Add Product",
        "active": "products"
    })

def admin_product_edit(request, pk):
    product = Product.objects.get(pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()

            messages.success(request, "Product updated successfully")  # ✅ HERE

            return redirect("admin_products")
    else:
        form = ProductForm(instance=product)

    return render(request, "gd_admin/product_form.html", {
        "form": form,
        "title": "Edit Product",
        "active": "products"
    })


def admin_product_delete(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()

    messages.success(request, "Product deleted successfully")  # ✅ HERE

    return redirect("admin_products")


def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, "gd_admin/category_list.html", {
        "categories": categories,
        "active": "categories"
    })

def admin_category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Category added successfully")  # ✅

            return redirect("admin_categories")
    else:
        form = CategoryForm()

    return render(request, "gd_admin/category_form.html", {
        "form": form,
        "title": "Add Category",
        "active": "categories"
    })


def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect("admin_categories")
    return render(request, "gd_admin/category_form.html", {"form": form, "title": "Edit Category"})

def admin_category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()

    messages.success(request, "Category deleted successfully")  # ✅

    return redirect("admin_categories")


@login_required
def admin_orders(request):
    orders = Order.objects.order_by("-created_at")

    return render(request, "gd_admin/order_list.html", {
        "orders": orders,
        "active": "orders"
    })

@login_required
def admin_order_detail(request, pk):
    order = Order.objects.get(pk=pk)
    items = order.items.all()

    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()

        messages.success(request, "Order status updated successfully")  # ✅ HERE

        return redirect("admin_order_detail", pk=order.id)

    return render(request, "gd_admin/order_detail.html", {
        "order": order,
        "items": items,
        "active": "orders"
    })

def admin_order_update_status(request, pk):
    order = get_object_or_404(Order, pk=pk)

    if request.method == "POST":
        order.status = request.POST.get("status")
        order.save()

    return redirect("admin_order_detail", pk=pk)

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def admin_create(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")  # ❌ error case
        else:
            user = User.objects.create_user(username=username, password=password)
            user.is_staff = True
            user.save()

            messages.success(request, "Admin created successfully")  # ✅ success

            return redirect("admin_list")

    return render(request, "gd_admin/admin_create.html", {
        "active": "admins"
    })

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def admin_list(request):
    admins = User.objects.filter(is_staff=True)

    return render(request, "gd_admin/admin_list.html", {
        "admins": admins,
        "active": "admins"
    })

@login_required
def admin_delete(request, pk):
    admin = User.objects.get(pk=pk)

    if admin != request.user:
        admin.delete()
        messages.success(request, "Admin removed successfully")  # ✅

    return redirect("admin_list")

