from django.utils import timezone

from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView, TemplateView, DeleteView
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Product, CustomUser, Purchase, Refund, CartItem, Cart, Category, Brand, Wishlist, Payment, Delivery, \
    Address, DeliveryService, PurchaseItem
from .forms import AuthenticationForm, UserCreationForm, ProductSearchForm, ShippingForm, AddressForm, \
    DeliveryServiceForm, PaymentForm, ProductUpdateForm, AddNewProductForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.db.models import Sum
from .mixins import SuperUserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .filters import ProductFilter
from decimal import Decimal

import json

from django.http import JsonResponse
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class Login(LoginView):
    next_page = 'profile'
    template_name = 'login.html'

    def get_success_url(self):
        return reverse_lazy(self.next_page)


class Register(CreateView):
    model = CustomUser
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('profile')


class Logout(LoginRequiredMixin, LogoutView):
    next_page = '/'
    login_url = 'login/'


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    login_url = '/login/'
    template_name = 'profile.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = self.request.user.purchases.all()

        purchase_list = []
        for purchase in purchases:
            items_with_total = []
            for item in purchase.items.all():
                items_with_total.append({
                    'product': item.product,
                    'quantity': item.quantity,
                    'total_price': item.product.price * item.quantity,
                })
            purchase_list.append({
                'purchase': purchase,
                'items': items_with_total,
            })

        context['purchase_list'] = purchase_list
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'main.html'
    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['iPhone16'] = Product.objects.get(name='iPhone 16 Pro Max 256 GB Black Titanium')
        context['MacbookAir'] = Product.objects.get(name='MacBook Air 13" M3 2024 Silver')
        context['MacbookPro'] = Product.objects.get(name='MacBook Pro 16" M4 PRO MAX Space Black')
        context['Playstation5'] = Product.objects.get(name='PlayStation 5 Pro Digital Edition')
        context['AppleVisionPro'] = Product.objects.get(name='Apple Vision Pro 256 GB')
        context['AirPodsMax'] = Product.objects.get(name='Apple AirPods Max Midnight')
        context['AppleWatch10'] = Product.objects.get(name='Apple Watch Series 10 42mm Jet Black')
        context['iPadPro'] = Product.objects.get(name='iPad Pro 13" 256GB M4 Silver')
        context['SamsungGalaxy'] = Product.objects.get(name='Samsung Galaxy Z Fold6 12GB/256GB Pink')

        context['category_list'] = Category.objects.all()

        if self.request.user.is_authenticated:
            context['wishlist_items'] = Wishlist.objects.filter(user=self.request.user).values_list('product_id',
                                                                                                    flat=True)
        else:
            context['wishlist_items'] = []

        discount_products = Product.objects.filter(discount_price__isnull=False)

        discount_paginator = Paginator(discount_products, 4)
        discount_page = self.request.GET.get("discount_page", 1)
        context["discounted_products"] = discount_paginator.get_page(discount_page)

        return context

class ProductsPageView(FilterView):
    model = Product
    template_name = 'products.html'
    paginate_by = 9
    filterset_class = ProductFilter
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['unique_memory_values'] = (Product.objects.values_list("built_in_memory", flat=True).distinct().order_by("built_in_memory"))
        context['unique_camera_values'] = (Product.objects.values_list("camera", flat=True).distinct().order_by("camera"))
        context['unique_ram_values'] = (Product.objects.values_list("ram", flat=True).distinct().order_by("ram"))
        if self.request.user.is_authenticated:
            context['wishlist_items'] = Wishlist.objects.filter(user=self.request.user).values_list('product_id',
                                                                                                    flat=True)
        else:
            context['wishlist_items'] = []
        return context


class ProductView(DetailView):
    model = Product
    template_name = 'product_id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        if product.category:
            context["breadcrumbs"] = product.category.get_breadcrumbs()
        else:
            context["breadcrumbs"] = []
        context["brand"] = product.brand

        return context


class ToggleWishlistView(LoginRequiredMixin, View):
    def post(self, request, product_id):
        try:
            product = get_object_or_404(Product, pk=product_id)



            wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

            if not created:
                wishlist_item.delete()

                return JsonResponse({"added": False})


            return JsonResponse({"added": True})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)




class ProductUpdate(SuperUserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'product_update_form.html'
    form_class = ProductUpdateForm
    success_url = '/'


class SearchProductsView(ListView):
    template_name = 'search_results.html'
    form_class = ProductSearchForm

    def get_queryset(self):
        query = self.request.GET.get('query', '')
        query_param = Q()
        if query:
            query_param = Q(name__icontains=query) | Q(description__icontains=query)
        return Product.objects.filter(query_param)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = self.form_class()
        return context


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact_us.html'


class WishListView(ListView):
    template_name = 'wishlist.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['wishlist_items'] = Wishlist.objects.filter(user_id=self.request.user)
        return context

class CategoryView(ListView):
    template_name = 'category.html'
    model = Category
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        return context


class BrandView(DetailView):
    template_name = 'brand.html'
    model = Brand
    context_object_name = 'brand'

    def get_queryset(self):
        return Brand.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.filter(brand_id=self.kwargs['pk'])
        return context

class CartItemView(CreateView):
    template_name = 'cart.html'
    model = CartItem

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        cart_count = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0

        return JsonResponse({"success": True, "cart_count": cart_count})



class CartView(ListView):
    template_name = 'cart.html'
    model = Cart
    def get_context_data(self, **kwargs):
        cart = get_object_or_404(Cart, user=self.request.user)
        cart_items = CartItem.objects.filter(cart=cart).select_related('product')

        for item in cart_items:
            item.total_price_per_item = item.product.price * item.quantity

        total_price = sum(item.product.price * item.quantity for item in cart_items)
        price_excl_VAT = total_price / Decimal("1.21")  # Без НДС 21%

        context = super().get_context_data(**kwargs)
        context['cart_items'] = cart_items
        context['total_price'] = round(total_price)
        context['price_excl_VAT'] = round(price_excl_VAT)

        user = self.request.user
        delivery = Delivery.objects.filter(purchase__user=user).first()
        context['delivery'] = delivery

        return context


class UpdateCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        product_id = self.kwargs["product_id"]
        data = json.loads(request.body)
        action = data.get("action")

        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
        if not cart_item:
            return JsonResponse({"error": "Товар не найден"}, status=404)

        print(f"Действие: {action}")
        print(f"CartItem перед изменением: {cart_item}")
        print(f"Количество ДО обновления: {cart_item.quantity}, Тип: {type(cart_item.quantity)}")

        if cart_item.quantity is None:
            cart_item.quantity = 0

        if action == "increase":
            cart_item.quantity += 1
        elif action == "decrease" and cart_item.quantity > 1:
            cart_item.quantity -= 1

        print(f"Количество ПОСЛЕ обновления: {cart_item.quantity}")

        cart_item.save(update_fields=["quantity"])
        cart_item.refresh_from_db()

        print(f"Количество ПОСЛЕ refresh_from_db: {cart_item.quantity}")
        total_price = sum(item.product.price * item.quantity for item in cart.items.all())
        price_excl_vat = total_price / Decimal("1.21")

        return JsonResponse({
            "quantity": cart_item.quantity,
            "item_total_price": cart_item.product.price * cart_item.quantity,
            "total_price": total_price,
            "price_excl_vat": int(round(price_excl_vat)),
        })

class DeleteCartItemView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()

        if cart_item:
            cart_item.delete()

        cart_count = CartItem.objects.filter(cart=cart).aggregate(Sum('quantity'))['quantity__sum'] or 0

        return JsonResponse({"success": True, "cart_count": cart_count})


class AddressFormView(FormView):
    template_name = 'address.html'
    form_class = AddressForm

    def get_initial(self):
        delivery = Delivery.objects.filter(purchase__user=self.request.user).first()
        initial = super().get_initial()

        if delivery and delivery.delivery_address:
            address = delivery.delivery_address
            initial.update({
                'country': address.country,
                'postal_code': address.postal_code,
                'city': address.city,
                'street': address.street,
                'house_number': address.house_number,
                'phone_number': address.phone_number,
            })

        return initial

    def form_valid(self, form):
        address = form.save()
        return redirect(reverse_lazy('checkout_delivery', kwargs={'address_id': address.id}))


class DeliveryCreateView(CreateView):
    model = Delivery
    fields = ['delivery_service']
    template_name = 'delivery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['delivery_service_form'] = DeliveryServiceForm()
        context['delivery_services'] = DeliveryService.objects.all()
        return context

    def form_valid(self, form):
        address_id = self.kwargs.get('address_id')
        purchase = Purchase.objects.create(user=self.request.user)
        form.instance.purchase = purchase
        form.instance.delivery_address_id = address_id
        super().form_valid(form)

        response = self.transfer_cart_items(purchase)
        if not response['success']:
            return JsonResponse(response)

        return redirect(self.get_success_url())

    def get_success_url(self):
        purchase_id = self.object.purchase.id
        return reverse_lazy('checkout_payment', kwargs={'purchase_id': purchase_id})

    def transfer_cart_items(self, purchase):
        cart = Cart.objects.filter(user=self.request.user).first()
        if not cart:
            return {'success': False, 'error': 'Cart is empty'}

        cart_items = CartItem.objects.filter(cart=cart)
        for cart_item in cart_items:
            PurchaseItem.objects.create(
                purchase=purchase,
                product=cart_item.product,
                quantity=cart_item.quantity,)

        cart_items.delete()

        return {'success': True}



class PaymentView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        purchase_id = self.kwargs.get('purchase_id')
        print(f"Purchase ID from session: {purchase_id}")
        if purchase_id:
            purchase = Purchase.objects.get(id=purchase_id)
            context['purchase'] = purchase
            context['cart_items'] = purchase.items.all()
            total_price = sum(item.product.price * item.quantity for item in purchase.items.all())
            context["total_price"] = round(total_price)
            price_excl_VAT = total_price / Decimal("1.21")
            context["price_excl_VAT"] = round(price_excl_VAT)
        else:
            context['purchase'] = None
            context['cart_items'] = []
            context["total_price"] = 0
            context["price_excl_VAT"] = 0

        return context

    def form_valid(self, form):
        purchase_id = self.kwargs.get("purchase_id")
        purchase = Purchase.objects.get(id=purchase_id)
        total_price = sum(item.product.price * item.quantity for item in purchase.items.all())

        form.instance.purchase = purchase
        form.instance.amount = total_price
        form.instance.status = 'pending'
        self.object = form.save()

        stripe_token = self.request.POST.get("stripeToken")

        if not stripe_token:
            return JsonResponse({"success": False, "error": "Invalid payment data"})

        print("CSRF Token from request:", self.request.POST.get("csrfmiddlewaretoken"))

        try:
            charge = stripe.Charge.create(
                amount=int(total_price * 100),
                currency="czk",
                source=stripe_token,
                description=f"Payment for purchase #{purchase.id}",
            )

            self.object.status = "completed"
            self.object.transaction_id = charge.id
            self.object.payment_date = timezone.now()
            self.object.save()

            return JsonResponse({"success": True, "redirect_url": reverse_lazy("payment_success")})

        except stripe.error.CardError as e:
            return JsonResponse({"success": False, "error": f"Card error: {e.error.message}"})
        except stripe.error.StripeError as e:
            return JsonResponse({"success": False, "error": f"Stripe error: {e.error.message}"})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)})

    def form_invalid(self, form):
        print("Form errors:", form.errors)
        return JsonResponse({"success": False, "error": "Invalid form data", "errors": form.errors})


class PaymentSuccessView(TemplateView):
    template_name = 'payment_success.html'


class AdminMenuListView(SuperUserPassesTestMixin, ListView):
    model = Product
    template_name = 'admin_menu.html'


class PopularProducts(DetailView):
    model = Product
    template_name = 'popular_products.html'


class SummerSale(DetailView):
    model = Product
    template_name = 'summer_sale.html'


class AddNewProduct(SuperUserPassesTestMixin, CreateView):
    model = Product
    template_name = 'add_new_product.html'
    form_class = AddNewProductForm
    success_url = '/'


