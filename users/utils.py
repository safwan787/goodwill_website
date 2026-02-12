from urllib.parse import quote

def get_order_whatsapp_url(order):
    whatsapp_number = "918075564099"

    message = f"""
🛒 New Order Received

Order ID: {order.id}
Customer: {order.customer_name}
Phone: {order.phone}
Email: {order.email}

Please check admin panel for details.
"""

    return f"https://wa.me/{whatsapp_number}?text={quote(message)}"
