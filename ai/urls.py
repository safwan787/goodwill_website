from django.urls import path
from . import views

urlpatterns = [
    path("product-description/", views.generate_product_description),
    path("category-description/", views.generate_category_description),
]
