from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

urlpatterns = [
    # Auth
    path('auth/register/',
         views.RegisterView.as_view(),     name='register'),
    path('auth/login/',
         TokenObtainPairView.as_view(),    name='login'),
    path('auth/refresh/',
         TokenRefreshView.as_view(),       name='token_refresh'),
    path('auth/profile/',
         views.profile_view,               name='profile'),

    # Categories
    path('categories/',
         views.CategoryListView.as_view(), name='categories'),

    # Products
    path('products/',
         views.ProductListView.as_view(),       name='products'),
    path('products/<int:pk>/',
         views.ProductDetailView.as_view(),     name='product-detail'),
    path('products/<int:pk>/similar/',
         views.similar_products,               name='similar'),
    path('products/<int:pk>/reviews/',
         views.ReviewListCreateView.as_view(),  name='reviews'),

    # Wishlist
    path('wishlist/',
         views.wishlist_view,                   name='wishlist'),
    path('wishlist/<int:pk>/toggle/',
         views.wishlist_toggle,                 name='wishlist-toggle'),

    # Cart
    path('cart/',
           views.cart_view,                       name='cart'),
    path('cart/add/<int:pk>/',
         views.cart_add,                        name='cart-add'),
    path('cart/update/<int:item_id>/',
         views.cart_update,                     name='cart-update'),
    path('cart/remove/<int:item_id>/',
         views.cart_remove,                     name='cart-remove'),
    path('cart/clear/',
         views.cart_clear,                      name='cart-clear'),

    # Orders
    path('orders/',
         views.OrderListView.as_view(),         name='orders'),
    path('orders/create/',
         views.create_order,                    name='create-order'),
    path('orders/<int:pk>/',
         views.OrderDetailView.as_view(),       name='order-detail'),

    # Stripe
    path('payment/create-intent/',
         views.create_payment_intent,           name='create-intent'),
    path('payment/confirm/',
         views.confirm_payment,                 name='confirm-payment'),
]