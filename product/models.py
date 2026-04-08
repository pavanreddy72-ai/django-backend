from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name
class Product(models.Model):
    title       = models.CharField(max_length=200)
    category    = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE)
    price       = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(0)])
    discount    = models.DecimalField(
        max_digits=5, decimal_places=2, default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True)
    image       = models.ImageField(upload_to='products/', null=True, blank=True)
    rating      = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    num_reviews = models.IntegerField(default=0)
    stock       = models.IntegerField(default=0)
    is_active   = models.BooleanField(default=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    @property
    def in_stock(self):
        return self.stock > 0

    def get_similar_products(self):
        return Product.objects.filter(
            category=self.category).exclude(id=self.id)[:4]


class Review(models.Model):
    product    = models.ForeignKey(
        Product, related_name='reviews', on_delete=models.CASCADE)
    user       = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE)
    rating     = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    title      = models.CharField(max_length=200, blank=True)
    comment    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')
def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        reviews = self.product.reviews.all()
        self.product.rating = reviews.aggregate(
            models.Avg('rating'))['rating__avg'] or 0
        self.product.num_reviews = reviews.count()
        self.product.save()


class Wishlist(models.Model):
    user     = models.OneToOneField(
        User, related_name='wishlist', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        Product, related_name='wishlisted_by', blank=True)
class Cart(models.Model):
    user       = models.OneToOneField(
        User, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
class CartItem(models.Model):
    cart     = models.ForeignKey(
        Cart, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(
        Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def subtotal(self):
        return self.product.discounted_price * self.quantity


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped',   'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user              = models.ForeignKey(

        User, related_name='orders', on_delete=models.CASCADE)
    status            = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price       = models.DecimalField(max_digits=12, decimal_places=2)
    shipping_address  = models.TextField()
    payment_method    = models.CharField(max_length=50, default='cod')
    stripe_payment_id = models.CharField(max_length=200, blank=True)
    is_paid           = models.BooleanField(default=False)
    paid_at           = models.DateTimeField(null=True, blank=True)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    order    = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product  = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True)
    name     = models.CharField(max_length=200)
    price    = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return float(self.price) * self.quantity