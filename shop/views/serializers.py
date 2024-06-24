# shop\views\serializers.py

from rest_framework import serializers
from ..models import  League, Category, User, Patch, Product, ProductImage, Order, OrderDetails, Review, Cart, CartItem, Wishlist, WishlistItem, Team
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from ..utils import generate_firebase_storage_url  # Make sure this is correctly imported

# Add other serializers as needed for your models

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Log the token payload for debugging
        print("Token Payload Before Adding Custom Data:", token.payload)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email
        token['is_Admin'] = user.is_superuser
        token['Name'] = user.first_name
        token['last_name'] = user.last_name
        token['phone_number'] = user.phone_number
        token['profile_picture'] = user.profile_picture

        # Log the token payload after modifications
        print("Token Payload After Adding Custom Data:", token.payload)

        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patch
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'

class OrderDetailsSerializer(serializers.ModelSerializer):
    product_snapshot = serializers.JSONField(read_only=True)
    price_at_purchase = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderDetails
        fields = ['order', 'product', 'quantity', 'price_at_purchase', 'product_snapshot', 'size', 'custom_name', 'custom_number', 'patches', 'notes']

    def validate_product(self, value):
        try:
            product = Product.objects.get(pk=value.id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Invalid pk \"{value.id}\" - object does not exist.")
        return product

    def create(self, validated_data):
        product = validated_data.get('product')
        validated_data['price_at_purchase'] = product.price
        validated_data['product_snapshot'] = {
            'name': product.name,
            'price': str(product.price),
            'main_image_url': product.main_image_url,
            'description': product.description,
            'category': product.category.name if product.category else None
        }
        return OrderDetails.objects.create(**validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        order = Order.objects.create(**validated_data)
        order.total_price = order.calculate_total_price()
        order.save()
        return order
            
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'
        

class LeagueSerializer(serializers.ModelSerializer):
    # image = serializers.SerializerMethodField(method_name='get_image_url')
    
    class Meta:
        model = League
        fields = '__all__'
    
    # def get_image_url(self, obj):
    #     """
    #     This method returns the full URL for the team's image stored in Firebase Storage.
    #     """
    #     if obj.image:  # Assuming 'image_name' is the field in your Team model that stores the image name
    #         return generate_firebase_storage_url(obj.image)
    #     return None
