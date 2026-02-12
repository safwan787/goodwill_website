# # ai/services.py

# import os
# from openai import OpenAI

# DEV_MODE = True  # 👈 turn OFF later when you add billing


# def generate_text(prompt):
#     if DEV_MODE:
#         # Demo / fallback AI response
#         return (
#             "This is a demo AI-generated description. "
#             "It highlights the category or product in a clear, "
#             "professional way and can be replaced with real AI output "
#             "once live API access is enabled."
#         )

#     api_key = os.getenv("OPENAI_API_KEY")

#     if not api_key:
#         return None

#     try:
#         client = OpenAI(api_key=api_key)

#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {
#                     "role": "system",
#                     "content": "You write clean, professional descriptions for an online store."
#                 },
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.7,
#             max_tokens=150,
#         )

#         return response.choices[0].message.content.strip()

#     except Exception:
#         return None

from .local_ai import (
    generate_category_description,
    generate_product_description,
)


def generate_text(prompt, mode="product"):
    """
    Local AI fallback (no external API)
    """

    if mode == "category":
        return generate_category_description(prompt)

    return generate_product_description(prompt)