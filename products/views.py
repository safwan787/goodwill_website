from django.shortcuts import render

# Create your views here.
from django.db.models import Q

from store_admin.models import Product, Category

def product_list(request):
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q')

    categories = Category.objects.all()
    products = Product.objects.all().order_by('-created_at')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if search_query:
        products = products.filter(name__icontains=search_query)

    return render(request, "user/product_list.html", {
        "categories": categories,
        "products": products,
        "search_query": search_query,
    })


def product_detail(request, id):
    product = Product.objects.get(id=id, available=True)
    return render(request, "user/product_detail.html", {"product": product})