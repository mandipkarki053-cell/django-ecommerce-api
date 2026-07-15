from rest_framework import serializers
from .models import Order, OrderItem, Product, Cart, CartItem, Category, User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=4)
    role = serializers.ChoiceField(
        choices=[
            ('buyer', 'Buyer'),
            ('seller', 'Seller'),
        ]
    )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class ViewProduct(serializers.ModelSerializer):
    seller = serializers.StringRelatedField()
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = '__all__'


class ViewCategory(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class ViewCart(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Cart
        fields = '__all__'


class ViewOrder(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Order
        fields = '__all__'


class ViewCartItem(serializers.ModelSerializer):
    cart = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = CartItem
        fields = '__all__'


class ViewOrderItem(serializers.ModelSerializer):
    product = serializers.StringRelatedField()
    order = serializers.StringRelatedField()

    class Meta:
        model = OrderItem
        fields = '__all__'
