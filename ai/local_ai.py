# ai/local_ai.py

import random


# -----------------------------
# CATEGORY DESCRIPTION ENGINE
# -----------------------------

CATEGORY_TEMPLATES = [
    "{name} products are designed to add elegance and meaning to special moments. This category offers thoughtfully crafted items suitable for gifting and decoration.",
    "The {name} category includes carefully selected products that combine quality, style, and emotional value, making them ideal for memorable occasions.",
    "{name} items are created to celebrate moments that matter. This category features products that blend creativity with lasting impressions.",
    "Explore our {name} collection, featuring products crafted to enhance personal spaces and meaningful celebrations."
]


def generate_category_description(name: str) -> str:
    template = random.choice(CATEGORY_TEMPLATES)
    return template.format(name=name.strip().title())


# -----------------------------
# PRODUCT DESCRIPTION ENGINE
# -----------------------------

PRODUCT_INTROS = [
    "This {name} is crafted to highlight elegance and lasting value.",
    "The {name} is designed to preserve meaningful moments with style.",
    "Our {name} combines thoughtful design with quality craftsmanship.",
    "This {name} offers a refined way to celebrate special memories."
]

PRODUCT_MIDDLES = [
    "Made with attention to detail, it enhances both personal and gift-worthy spaces.",
    "Its refined finish and balanced design make it suitable for a variety of occasions.",
    "The product reflects careful craftsmanship and a timeless appeal.",
    "It is created to complement modern interiors while holding emotional significance."
]

PRODUCT_ENDINGS = [
    "A perfect choice for gifting or personal use.",
    "Ideal for marking special moments and celebrations.",
    "An excellent addition to any meaningful collection.",
    "A thoughtful option for those who value quality and sentiment."
]


def generate_product_description(name: str) -> str:
    intro = random.choice(PRODUCT_INTROS)
    middle = random.choice(PRODUCT_MIDDLES)
    ending = random.choice(PRODUCT_ENDINGS)

    return f"{intro.format(name=name.strip().title())} {middle} {ending}"
