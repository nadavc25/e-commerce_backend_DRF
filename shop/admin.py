from django.contrib import admin
from .models import Brand, Collection, SportType, League, Team, Gender, SizeTypeCategory, ClothCategory, Season, Product, Patch, ProductImage, Order, OrderDetails, Review, Cart, CartItem, Wishlist, WishlistItem

# Register your models here.
admin.site.register([Brand,
                    Collection, 
                    SportType, 
                    League, 
                    Team, 
                    Gender, 
                    SizeTypeCategory, 
                    ClothCategory,
                    Season, 
                    Product,
                    Patch, 
                    ProductImage, 
                    Order, 
                    OrderDetails, 
                    Review, 
                    Cart, 
                    CartItem, 
                    Wishlist,
                    WishlistItem
                    ])
