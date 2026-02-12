from django.urls import path
from . import views

urlpatterns = [
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path("products/", views.admin_product_list, name="admin_products"),
    path("products/add/", views.admin_product_add, name="admin_product_add"),
    path("products/edit/<int:pk>/", views.admin_product_edit, name="admin_product_edit"),
    path("products/delete/<int:pk>/", views.admin_product_delete, name="admin_product_delete"),
    path("categories/", views.admin_category_list, name="admin_categories"),
    path("categories/add/", views.admin_category_add, name="admin_category_add"),
    path("categories/edit/<int:pk>/", views.admin_category_edit, name="admin_category_edit"),
    path("categories/delete/<int:pk>/", views.admin_category_delete, name="admin_category_delete"),
    path("orders/", views.admin_orders, name="admin_orders"),
    path("orders/<int:pk>/", views.admin_order_detail, name="admin_order_detail"),
    path("orders/<int:pk>/status/", views.admin_order_update_status, name="admin_order_update_status"),
    path("admins/add/", views.admin_create, name="admin_create"),
    path("admins/", views.admin_list, name="admin_list"),
    path("admins/delete/<int:pk>/", views.admin_delete, name="admin_delete"),




]
