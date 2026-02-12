from django.urls import path
from . import views

urlpatterns = [

    # ================= HOME =================
    path("", views.home, name="home"),

    # ================= AUTH =================
    path("login/", views.user_login, name="login"),
    path("register/", views.user_register, name="register"),
    path("logout/", views.user_logout, name="logout"),

    # ================= PRODUCTS & INQUIRY =================
    path("inquiry/<int:product_id>/", views.inquiry_page, name="inquiry_page"),
    path("inquiry-success/", views.inquiry_success, name="inquiry_success"),

    # ================= CART =================
    path("cart/", views.cart, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/update/<int:product_id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:product_id>/", views.remove_from_cart, name="remove_from_cart"),
    
    path("buy-now/<int:product_id>/", views.buy_now, name="buy_now"),
    # ================= CHECKOUT (CART BASED ONLY) =================
    path("cart/checkout/", views.cart_checkout, name="cart_checkout"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),

    # ================= DASHBOARD =================
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/enquiries/", views.dashboard_enquiries, name="dashboard_enquiries"),
    path("dashboard/orders/", views.dashboard_orders, name="dashboard_orders"),
    path("dashboard/addresses/", views.dashboard_addresses, name="dashboard_addresses"),

    # ================= STATIC / INFO =================
    path("offers/", views.offers, name="offers"),
    path("raise-problem/", views.raise_problem, name="raise_problem"),

    # ================= DESIGN SERVICES =================
    path("services/poster-design/", views.poster_design, name="poster_design"),
    path("design-enquiry/", views.design_inquiry, name="design_inquiry"),
]
