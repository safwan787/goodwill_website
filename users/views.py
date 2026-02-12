from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import quote

from store_admin.models import Product, Category, Order, OrderItem, Inquiry
from .models import Address
from .forms import InquiryForm
def home(request):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True).order_by('-created_at')[:6]

    return render(request, "user/home.html", {
        "categories": categories,
        "products": products,
    })
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")

        messages.error(request, "Invalid username or password")

    return render(request, "user/login.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created. Please login.")
        return redirect("login")

    return render(request, "user/register.html")


def user_logout(request):
    logout(request)
    return redirect("home")

def cart(request):
    cart = request.session.get('cart', {})
    return render(request, "user/cart.html", {"cart": cart})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)

    cart = request.session.get('cart', {})
    pid = str(product.id)

    if pid in cart:
        cart[pid]['qty'] += 1
    else:
        cart[pid] = {
            "name": product.name,
            "price": float(product.price),
            "qty": 1
        }

    request.session['cart'] = cart
    return redirect("cart")


def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        action = request.GET.get("action")
        if action == "increase":
            cart[pid]['qty'] += 1
        elif action == "decrease":
            cart[pid]['qty'] -= 1
            if cart[pid]['qty'] <= 0:
                del cart[pid]

    request.session['cart'] = cart
    return redirect("cart")


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    request.session['cart'] = cart
    return redirect("cart")

@login_required
def cart_checkout(request):
    cart = request.session.get("cart", {})
    addresses = Address.objects.filter(user=request.user)

    if not cart:
        return redirect("cart")

    if request.method == "POST":
        address_id = request.POST.get("address_id")

        if address_id:
            addr = get_object_or_404(Address, id=address_id, user=request.user)
            full_address = f"{addr.address_line}, {addr.city}, {addr.state} - {addr.pincode}"
        else:
            full_address = f"{request.POST.get('address_line')}, {request.POST.get('city')}, {request.POST.get('state')} - {request.POST.get('pincode')}"

        order = Order.objects.create(
            customer_name=request.user.username,
            phone="",
            email=request.user.email,
            address=full_address,
            status="pending"
        )

        for pid, item in cart.items():
            product = get_object_or_404(Product, id=pid)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['qty'],
                price=item['price']
            )

            product.stock -= item['qty']
            product.save()

        request.session.pop("cart", None)
        return redirect("order_success", order_id=order.id)

    return render(request, "user/cart_checkout.html", {
        "cart": cart,
        "addresses": addresses
    })

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, email=request.user.email)
    return render(request, "user/order_success.html", {"order": order})

from store_admin.models import Product, Inquiry, InquiryAttachment
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import InquiryForm


def inquiry_page(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)

    if request.method == "POST":
        form = InquiryForm(request.POST)

        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()

            # ✅ Handle single file upload manually
            uploaded_file = request.FILES.get("file")

            if uploaded_file:
                InquiryAttachment.objects.create(
                    inquiry=inquiry,
                    file=uploaded_file,
                    description="Product reference"
                )

            # ✅ Send email to admin
            send_mail(
                subject=f"New Product Inquiry – {product.name}",
                message=f"""
New Product Inquiry

Product: {product.name}
Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone}

Message:
{inquiry.message}

Attachment:
{'Yes (check admin panel)' if uploaded_file else 'No'}
""",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )

            # ✅ Save for WhatsApp session
            request.session["last_inquiry"] = {
                "product": product.name,
                "name": inquiry.name,
                "message": inquiry.message,
            }

            return redirect("inquiry_success")

    else:
        form = InquiryForm()

    return render(request, "user/inquiry.html", {
        "product": product,
        "form": form
    })


def inquiry_success(request):
    data = request.session.get("last_inquiry")

    message = f"""
New Inquiry

Product: {data.get('product')}
Name: {data.get('name')}

Message:
{data.get('message')}
""" if data else "New enquiry received."

    whatsapp_url = f"https://wa.me/918075564099?text={quote(message)}"
    request.session.pop("last_inquiry", None)

    return render(request, "user/inquiry_success.html", {
        "whatsapp_url": whatsapp_url
    })

def poster_design(request):
    return render(request, "user/poster_design.html")


from store_admin.models import Inquiry, InquiryAttachment
from django.core.mail import send_mail
from django.conf import settings
from urllib.parse import quote

def design_inquiry(request):
    if request.method == "POST":

        inquiry = Inquiry.objects.create(
            name=request.POST.get("name"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            message=request.POST.get("message"),
        )

        files = request.FILES.getlist("files")

        for f in files:
            InquiryAttachment.objects.create(
                inquiry=inquiry,
                file=f,
                description=request.POST.get(f"{f.name}_desc", "")
            )

        # EMAIL
        send_mail(
            subject="New Poster Design Inquiry",
            message=f"""
New Design Inquiry

Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone}

Message:
{inquiry.message}

Attachments: Check admin panel.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=True,
        )

        # WhatsApp message
        message = f"""
New Design Inquiry

Name: {inquiry.name}
Phone: {inquiry.phone}
Message: {inquiry.message}
"""

        whatsapp_url = f"https://wa.me/918075564099?text={quote(message)}"

        request.session["whatsapp_url"] = whatsapp_url

        return redirect("inquiry_success")

    return redirect("poster_design")



@login_required
def dashboard(request):
    return render(request, "user/dashboard.html")


@login_required
def dashboard_enquiries(request):
    enquiries = Inquiry.objects.filter(email=request.user.email).order_by("-created_at")
    return render(request, "user/dashboard_enquiries.html", {"enquiries": enquiries})


@login_required
def dashboard_orders(request):
    orders = Order.objects.filter(email=request.user.email).order_by("-created_at")
    return render(request, "user/dashboard_orders.html", {"orders": orders})


@login_required
def dashboard_addresses(request):
    addresses = Address.objects.filter(user=request.user)

    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            label=request.POST.get("label"),
            address_line=request.POST.get("address_line"),
            city=request.POST.get("city"),
            state=request.POST.get("state"),
            pincode=request.POST.get("pincode"),
        )
        return redirect("dashboard_addresses")

    return render(request, "user/dashboard_addresses.html", {"addresses": addresses})

def offers(request):
    return render(request, "user/offers.html")


def raise_problem(request):
    return render(request, "user/raise_problem.html")

from django.shortcuts import redirect, get_object_or_404
from store_admin.models import Product

def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)

    cart = request.session.get('cart', {})
    pid = str(product.id)

    cart[pid] = {
        "name": product.name,
        "price": float(product.price),
        "qty": 1
    }

    request.session['cart'] = cart

    return redirect('cart_checkout')

