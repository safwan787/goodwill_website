from django.db import models

# Create your models here.

from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    
    stock = models.PositiveIntegerField(default=0)   # 👈 NEW

    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Inquiry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ("new", "New"),
            ("reviewing", "Reviewing"),
            ("quoted", "Quoted"),
            ("completed", "Completed"),
        ],
        default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class InquiryAttachment(models.Model):
    inquiry = models.ForeignKey(Inquiry, on_delete=models.CASCADE, related_name="attachments")
    file = models.FileField(upload_to="inquiries/")
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Attachment for {self.inquiry.name}"



class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    address = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('confirmed', 'Confirmed'),
            ('shipped', 'Shipped'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.customer_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


