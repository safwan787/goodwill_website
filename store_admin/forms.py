from django import forms
from .models import Product
from .models import Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "stock",
            "image",
            "available",
        ]

        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }