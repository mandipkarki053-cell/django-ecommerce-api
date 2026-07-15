from django.shortcuts import render
from rest_framework.permissions import IsAdminUser, AllowAny, BasePermission
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from .models import User, Product, Order, OrderItem, Cart, CartItem, Category
from .serializers import (
    ProductSerializer,
    ViewOrder,
    ViewCategory,
    ViewCart,
    ViewCartItem,
    CartItemSerializer,
    CartSerializer,
    ViewProduct,
    LoginSerializer,
    RegisterSerializer,

    CategorySerializer,
)
from django.contrib.auth import authenticate
from django.db import transaction


@api_view(['POST'])
def register(request):
    check = RegisterSerializer(data=request.data)
    if not check.is_valid():
        return Response(check.errors)
    username = check.validated_data['username']
    password = check.validated_data['password']
    role = check.validated_data['role']

    if User.objects.filter(username=username).exists():
        return Response({'Message': 'Username Already Exists'}, status=409)
    User.objects.create_user(username=username, password=password, role=role)
    return Response({'Message': 'Successfully Registered'}, status=201)


@api_view(['POST'])
def login(request):
    check = LoginSerializer(data=request.data)
    if not check.is_valid():
        return Response(check.errors, status=400)
    username = check.validated_data['username']
    password = check.validated_data['password']
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'Messsage': 'Wrong Username and Password'}, status=401)
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    })


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.role == 'seller')

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    filterset_fields = ['name', 'price', 'description', 'category', 'stock']
    search_fields = ['name']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViewProduct
        return ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsSeller()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    filterset_fields = ['name']
    search_fields = ['name']
    ordering_fields = ['name']

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViewCategory
        return CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViewCartItem
        return CartItemSerializer

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart = Cart.objects.get(user=self.request.user)
        serializer.save(cart=cart)


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ViewCart
        return CartSerializer

    def get_permissions(self):
        return [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderViewSet(ReadOnlyModelViewSet):
    queryset = Order.objects.all()
    serializer_class = ViewOrder
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout(request):

    with transaction.atomic():

        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return Response(
                {'message': 'Cart is empty'},
                status=400
            )

        order = Order.objects.create(user=request.user)

        total = 0

        for item in cart_items:

            product = item.product

            if item.quantity > product.stock:
                return Response(
                    {
                        "message": f"{product.name} is out of stock"
                    },
                    status=400
                )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )

            total += product.price * item.quantity

            product.stock -= item.quantity
            product.save()

        order.total_price = total
        order.save()

        cart_items.delete()

        return Response(
            {
                "message": "Order placed successfully",
                "order_id": order.id,
                "total_price": total
            },
            status=201
        )
