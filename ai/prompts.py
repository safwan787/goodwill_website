# ai/prompts.py

def product_description_prompt(name, material=None, occasion=None):
    """
    Generates a prompt for creating a product description.
    """

    base_prompt = (
        "Write a short, clear, and attractive product description "
        "for an online store. The tone should be professional, friendly, "
        "and suitable for customers. Avoid emojis."
    )

    details = f"\nProduct Name: {name}"

    if material:
        details += f"\nMaterial: {material}"

    if occasion:
        details += f"\nOccasion: {occasion}"

    closing = (
        "\n\nThe description should highlight quality and usefulness, "
        "and be easy to read. Limit it to one short paragraph."
    )

    return base_prompt + details + closing


def category_description_prompt(category_name):
    """
    Generates a prompt for creating a category description.
    """

    return (
        "Write a short and engaging category description for an online store.\n"
        f"Category Name: {category_name}\n\n"
        "The description should explain what products belong in this category, "
        "be customer-friendly, and limited to 2–3 sentences."
    )
