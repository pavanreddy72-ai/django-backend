from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
import stripe
from django.conf import settings
from .models import Category, Product, Review, Wishlist, Cart, CartItem, Order, OrderItem
from .serializer import *

stripe.api_key = settings.STRIPE_SECRET_KEY

class RegisterView(generics.CreateAPIView):
    serializer_class   = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Cart.objects.create(user=user)
        Wishlist.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'user':    UserSerializer(user).data,
            'access':  str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)
@api_view(['GET', 'PUT'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    if request.method == 'GET':
        return Response(UserSerializer(request.user).data)
    serializer = UserSerializer(
        request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


# ── CATEGORIES ─────────────────────────────────────────────
class CategoryListView(generics.ListCreateAPIView):
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
class ProductListView(generics.ListCreateAPIView):
    serializer_class   = ProductListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter,
                          filters.OrderingFilter]
    filterset_fields   = ['category__slug', 'is_active']
    search_fields      = ['title', 'description', 'category__name']
    ordering_fields    = ['price', 'rating', 'created_at']
    ordering           = ['-created_at']

    def get_queryset(self):
        qs = Product.objects.filter(is_active=True)
        p  = self.request.query_params
        if p.get('min_price'):
            qs = qs.filter(price__gte=p['min_price'])
        if p.get('max_price'):
            qs = qs.filter(price__lte=p['max_price'])
        if p.get('min_rating'):
            qs = qs.filter(rating__gte=p['min_rating'])
        if p.get('in_stock') == 'true':
            qs = qs.filter(stock__gt=0)
        return qs
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset           = Product.objects.all()
    serializer_class   = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def similar_products(request, pk):
    product = generics.get_object_or_404(Product, pk=pk)
    return Response(ProductListSerializer(
        product.get_similar_products(), many=True).data)
class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        return [permissions.AllowAny()] if self.request.method == 'GET' \
               else [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['pk'])

    def perform_create(self, serializer):
        product = generics.get_object_or_404(Product, pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, product=product)
@api_view(['GET'])
def wishlist_view(request):
    wl, _ = Wishlist.objects.get_or_create(user=request.user)
    return Response(WishlistSerializer(wl).data)


@api_view(['POST'])
def wishlist_toggle(request, pk):
    product = generics.get_object_or_404(Product, pk=pk)
    wl, _   = Wishlist.objects.get_or_create(user=request.user)
    if wl.products.filter(id=pk).exists():
        wl.products.remove(product)
        return Response({'status': 'removed'})
    wl.products.add(product)
    return Response({'status': 'added'})
@api_view(['GET'])
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return Response(CartSerializer(cart).data)


@api_view(['POST'])
def cart_add(request, pk):
    product  = generics.get_object_or_404(Product, pk=pk)
    cart, _  = Cart.objects.get_or_create(user=request.user)
    quantity = int(request.data.get('quantity', 1))
    if quantity > product.stock:
        return Response({'error': 'Not enough stock.'}, status=400)
    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    item.quantity = quantity if created else min(
        item.quantity + quantity, product.stock)
    item.save()
    return Response(CartSerializer(cart).data)
@api_view(['PUT'])
def cart_update(request, item_id):
    item     = generics.get_object_or_404(
        CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.data.get('quantity', 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = min(quantity, item.product.stock)
        item.save()
    return Response(CartSerializer(item.cart).data)


@api_view(['DELETE'])
def cart_remove(request, item_id):
    item = generics.get_object_or_404(
        CartItem, id=item_id, cart__user=request.user)
    cart = item.cart
    item.delete()
    return Response(CartSerializer(cart).data)
@api_view(['DELETE'])
def cart_clear(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart.items.all().delete()
    return Response({'detail': 'Cart cleared.'})


# ── ORDERS ─────────────────────────────────────────────────
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
@api_view(['POST'])
def create_order(request):
    serializer = CreateOrderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    cart = generics.get_object_or_404(Cart, user=request.user)
    if not cart.items.exists():
        return Response({'error': 'Cart is empty.'}, status=400)
    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price,
        shipping_address=serializer.validated_data['shipping_address'],
        payment_method=serializer.validated_data['payment_method'],
    )
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            name=item.product.title,
            price=item.product.discounted_price,
            quantity=item.quantity,
        )
        item.product.stock -= item.quantity
        item.product.save()
    cart.items.all().delete()
    return Response(OrderSerializer(order).data, status=201)
@api_view(['POST'])
def create_payment_intent(request):
    order = generics.get_object_or_404(
        Order, pk=request.data.get('order_id'), user=request.user)
    intent = stripe.PaymentIntent.create(
        amount=int(float(order.total_price) * 100),
        currency='usd',
        metadata={'order_id': order.id}
    )
    return Response({'client_secret': intent.client_secret})


@api_view(['POST'])
def confirm_payment(request):
    from django.utils import timezone
    order = generics.get_object_or_404(
        Order, pk=request.data.get('order_id'), user=request.user)
    order.is_paid           = True
    order.status            = 'confirmed'
    order.stripe_payment_id = request.data.get('payment_intent_id', '')
    order.paid_at           = timezone.now()
    order.save()
    return Response(OrderSerializer(order).data)
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.filter(is_active=True)
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = ProductListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)