"""
URL configuration for diploma_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from myapp.views import Login, Register, Logout, ProfileView, ProductUpdate, AddNewProduct, ProductListView, \
    ProductsPageView, ProductView, ToggleWishlistView, DeleteWishlistItemView, AboutView, ContactView, WishListView, \
    CartItemView, CartView, UpdateCartView, DeliveryCreateView, DeleteCartItemView, PaymentSuccessView, CategoryView, \
    BrandView, PopularProducts, SummerSaleView, AddressFormView, PaymentView, SearchProductsView, RefundView, RefundRequestView, \
    RefundListView, RefundAcceptView, RefundDeclineView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ProductListView.as_view(), name='main'),
    path('products/', ProductsPageView.as_view(), name='products'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_id'),
    path('product_update/<int:pk>/', ProductUpdate.as_view(), name='product_update'),
    path('category/<int:pk>/', CategoryView.as_view(), name='category_id'),
    path('brand/<int:pk>/', BrandView.as_view(), name='brand_id'),
    path('wishlist/toggle/<int:product_id>/', ToggleWishlistView.as_view(), name='toggle_wishlist'),
    path('wishlist/delete/<int:product_id>/', DeleteWishlistItemView.as_view(), name='delete_wishlist'),
    path('cart_item/', CartItemView.as_view(), name='cart_item'),
    path('search/', SearchProductsView.as_view(), name='search_products'),
    path('admin_menu/', include('myapp.admin_menu')),
    path('add_new_product/', AddNewProduct.as_view(), name='add_new_product'),
    path('about', AboutView.as_view(), name='about'),
    path('contact_us', ContactView.as_view(), name='contact_us'),
    path('wishlist', WishListView.as_view(), name='wishlist'),
    path('cart', CartView.as_view(), name='cart'),
    path('cart/update/<int:product_id>/', UpdateCartView.as_view(), name='update_cart'),
    path('cart/delete/<int:product_id>/', DeleteCartItemView.as_view(), name='delete_cart_item'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('login/', Login.as_view(), name='login'),
    path('register/', Register.as_view(), name='register'),
    path('logout/', Logout.as_view(), name='logout'),
    path('popular_products', PopularProducts.as_view(), name='popular_products'),
    path('summer_sale', SummerSaleView.as_view(), name='summer_sale'),
    path('checkout/address/', AddressFormView.as_view(), name='checkout_address'),
    path('checkout/delivery/<int:address_id>/', DeliveryCreateView.as_view(), name='checkout_delivery'),
    path('checkout/payment/<int:purchase_id>/', PaymentView.as_view(), name='checkout_payment'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('refund/<int:purchase_id>/', RefundView.as_view(), name='refund'),
    path('refund_request/<int:purchase_id>/', RefundRequestView.as_view(), name='refund_request'),
    path('refund/success/', TemplateView.as_view(template_name='refund_success.html'), name='refund_success'),
    path('view_refunds', RefundListView.as_view(), name='view_refunds'),
    path('refund_accept', RefundAcceptView.as_view(), name='refund_accept'),
    path('refund_decline', RefundDeclineView.as_view(), name='refund_decline'),

]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


