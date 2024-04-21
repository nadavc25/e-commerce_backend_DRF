# models.py
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

# User Model
class User(AbstractUser):
    firebase_uid = models.CharField(max_length=128, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    newsletter_subscribed = models.BooleanField(default=False)
    account_status = models.CharField(max_length=10, default='active', choices=(('active', 'Active'), ('suspended', 'Suspended')))
    profile_picture = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'custom_user'

class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Collection Model
class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)
    brand = models.ForeignKey(Brand, related_name='collections', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}"
    
# Sport Type Model
class SportType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Check if the slug already exists and modify it if necessary
            original_slug = self.slug
            counter = 1
            while SportType.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# League Model
class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    sport_type = models.ForeignKey(SportType, related_name='leagues', on_delete=models.CASCADE)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Team Model
class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, related_name='teams', on_delete=models.CASCADE)
    image = models.URLField(blank=True, null=True)
    collection = models.ForeignKey(Collection, related_name='teams', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
    
# Gender Model
class Gender(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Size Category Model
class SizeTypeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

# Cloth Category Model
class ClothCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Season Model
class Season(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Category model
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Product model
class Product(models.Model):
    MAX_SIZE_CHOICES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('2XL', 'Extra Large'),
        ('3XL', 'Extra Large'),
        ('4XL', 'Extra Large'),
    )

    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    max_available_size = models.CharField(max_length=3, choices=MAX_SIZE_CHOICES)
    main_image_url = models.URLField(blank=True, null=True)  # URL of the main image stored in Firebase Storage
    sport_type = models.ForeignKey(SportType, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
    size_category = models.ForeignKey(SizeTypeCategory, on_delete=models.CASCADE)#adult/ kids
    cloth_category = models.ForeignKey(ClothCategory, on_delete=models.CASCADE) #player version, polo, jacket...
    season = models.ForeignKey(Season, on_delete=models.CASCADE) #summer/winter
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, blank=True, null=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # If no slug, generate one
            base_slug = slugify(self.name)
            new_slug = base_slug
            num = 1
            while Product.objects.filter(slug=new_slug).exists():
                new_slug = f'{base_slug}-{num}'
                num += 1
            self.slug = new_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - Up to {self.max_available_size}"
    
    class Meta:
        # Assuming you want each product to be unique by these combined attributes
        unique_together = ('name',)

# Patch model
class Patch(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    available = models.BooleanField(default=True)  # Track availability
    popularity = models.IntegerField(default=0)    # Track popularity

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image_url = models.URLField(blank=True, null=True) # URL of the image stored in Firebase Storage
    alt_text = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"

# Order model
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def calculate_total_price(self):
        total_price = sum([item.price_at_purchase * item.quantity for item in self.items.all()])
        return total_price
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    custom_name = models.CharField(max_length=50, blank=True, null=True)  # For custom name printing
    custom_number = models.IntegerField(blank=True, null=True)  # For custom number printing
    patches = models.ManyToManyField(Patch, blank=True)  # Many patches can be selected

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in {self.order}"

# Review model
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.TextField()
    rating = models.PositiveIntegerField()
    review_image = models.URLField( blank=True, null=True, help_text="Upload an image with your review")

    class Meta:
        unique_together = ['user', 'product']

    def __str__(self):
        return f"Review by {self.user.username} on {self.product.name}"

# Cart model
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    items = models.ManyToManyField(Product, through='CartItem')

    def calculate_subtotal(self):
        subtotal = sum([item.product.price * item.quantity for item in self.cartitem_set.all()])
        return subtotal

    def __str__(self):
        return f"{self.user.username}'s Cart"
# CartItem model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
# Wishlist model
class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey('Wishlist', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['wishlist', 'product']

    def __str__(self):
        return f"{self.product.name} in {self.wishlist.user.username}'s Wishlist"
