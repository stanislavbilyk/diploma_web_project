from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MinValueValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_email_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    brands = models.ManyToManyField(Brand, blank=True)

    def get_breadcrumbs(self):
        categories = []
        category = self
        while category:
            categories.append(category)
            category = category.parent
        return list(reversed(categories))

    def __str__(self):
        return self.name


class Color(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class OS(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    quantity_on_storage = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)
    os = models.ForeignKey(OS, on_delete=models.CASCADE, null=True, blank=True)
    built_in_memory = models.IntegerField(null=True, blank=True)
    screen_diagonal = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    battery_capacity = models.IntegerField(null=True, blank=True)
    camera = models.IntegerField(null=True, blank=True)
    processor = models.CharField(max_length=255, null=True, blank=True)
    ram = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price

    def get_old_price(self):
        return self.price if self.has_discount() else None


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"



class Purchase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='purchases', null=True)
    time_of_purchase = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Purchase {self.id} by {self.user}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='purchases', null=True)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Purchase {self.purchase.id}"


class Refund(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='refund', null=True)
    time_of_refund = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.street}, {self.house_number}, {self.city}, {self.country}"


class DeliveryService(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Delivery(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='delivery')
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('in_transit', 'In transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    delivery_address = models.OneToOneField(Address, on_delete=models.CASCADE, null=True, blank=True)
    delivery_service = models.ForeignKey(DeliveryService, on_delete=models.CASCADE)
    tracking_number = models.CharField(max_length=100, null=True, blank=True)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Delivery for {self.purchase}"

class Payment(models.Model):
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE, related_name='payment')
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ], default='pending')
    payment_method = models.CharField(max_length=100, choices=[
        ('credit_card', 'Credit card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank transfer'),
        ('cash_on_delivery', 'Cash on delivery'),
    ])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Payment for {self.purchase} - {self.status}"


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wishlists')
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"Wishlist of {self.user} - {self.product}"


class TestTransaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("completed", "Completed"), ("failed", "Failed")])
    created_at = models.DateTimeField(auto_now_add=True)






