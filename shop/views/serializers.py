# shop\views\serializers.py

from rest_framework import serializers
from ..models import League, Category, User, Patch, Product, ProductImage, Order, OrderDetails, Review, Cart, CartItem, Wishlist, WishlistItem, Team
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
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity', 'price_at_purchase', 'custom_name', 'custom_number', 'patches']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderDetailsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'order_date', 'status', 'items']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderDetails.objects.create(order=order, **item_data)
        return order

    def validate(self, data):
        # Example validation: ensure there are items in the order
        if not data.get('items'):
            raise serializers.ValidationError("The order must include at least one item.")
        return data
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
