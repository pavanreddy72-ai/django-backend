from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Product, Review, Wishlist, Cart, CartItem, Order, OrderItem


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'password', 'password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        return User.objects.create_user(**validated_data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'image', 'products_count']

    def get_products_count(self, obj):
        return obj.products.filter(is_active=True).count()


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model  = Review
        fields = ['id', 'user', 'rating', 'title', 'comment', 'created_at']
        read_only_fields = ['user']

class ProductListSerializer(serializers.ModelSerializer):
    category         = CategorySerializer(read_only=True)
    discounted_price = serializers.ReadOnlyField()
    in_stock         = serializers.ReadOnlyField()

    class Meta:
        model  = Product
        fields = ['id', 'title', 'category', 'price', 'discount',
                  'discounted_price', 'image', 'rating', 'num_reviews', 'in_stock']


class ProductSerializer(serializers.ModelSerializer):
    category         = CategorySerializer(read_only=True)
    category_id      = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True)
    reviews          = ReviewSerializer(many=True, read_only=True)
    discounted_price = serializers.ReadOnlyField()
    in_stock         = serializers.ReadOnlyField()
    is_wishlisted    = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = ['id', 'title', 'category', 'category_id', 'price',
                  'discount', 'discounted_price', 'description', 'image',
                  'rating', 'num_reviews', 'stock', 'in_stock', 'is_active',
                  'reviews', 'is_wishlisted', 'created_at']
        
def get_is_wishlisted(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            wl = Wishlist.objects.filter(user=request.user).first()
            return wl.products.filter(id=obj.id).exists() if wl else False
        return False


class CartItemSerializer(serializers.ModelSerializer):
    product  = ProductListSerializer(read_only=True)
    subtotal = serializers.ReadOnlyField()

    class Meta:
        model  = CartItem
        fields = ['id', 'product', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    items       = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()
class Meta:
        model  = Cart
        fields = ['id', 'items', 'total_price', 'total_items', 'updated_at']


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model  = Wishlist
        fields = ['id', 'products']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OrderItem
        fields = ['id', 'name', 'price', 'quantity', 'subtotal']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user  = UserSerializer(read_only=True)

    class Meta:
        model  = Order
        fields = ['id', 'user', 'status', 'total_price', 'shipping_address',
                  'payment_method', 'is_paid', 'paid_at', 'items', 'created_at']
        read_only_fields = ['user', 'total_price', 'is_paid']


class CreateOrderSerializer(serializers.Serializer):
    shipping_address = serializers.CharField()
    payment_method   = serializers.CharField(default='cod')