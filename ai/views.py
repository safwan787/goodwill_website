from django.shortcuts import render

# Create your views here.
# ai/views.py

import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test

from .prompts import (
    product_description_prompt,
    category_description_prompt,
)
from .services import generate_text


def is_admin(user):
    return user.is_staff


@login_required
@user_passes_test(is_admin)
@require_POST
def generate_product_description(request):
    """
    Generate AI product description
    (Admin only)
    """
    try:
        data = json.loads(request.body)

        name = data.get("name")
        material = data.get("material")
        occasion = data.get("occasion")

        if not name:
            return JsonResponse(
                {"success": False, "error": "Product name is required"},
                status=400,
            )

        prompt = product_description_prompt(
            name=name,
            material=material,
            occasion=occasion,
        )

        description = generate_text(name, mode="product")


        if not description:
            return JsonResponse(
                {"success": False, "error": "AI generation failed"},
                status=500,
            )

        return JsonResponse(
            {"success": True, "description": description}
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )


@login_required
@user_passes_test(is_admin)
@require_POST
def generate_category_description(request):
    """
    Generate AI category description
    (Admin only)
    """
    try:
        data = json.loads(request.body)

        category_name = data.get("category_name")

        if not category_name:
            return JsonResponse(
                {"success": False, "error": "Category name is required"},
                status=400,
            )

        prompt = category_description_prompt(category_name)

        description = generate_text(category_name, mode="category")

        if not description:
            return JsonResponse(
                {"success": False, "error": "AI generation failed"},
                status=500,
            )

        return JsonResponse(
            {"success": True, "description": description}
        )

    except Exception as e:
        return JsonResponse(
            {"success": False, "error": str(e)},
            status=500,
        )
