from django.contrib import messages
from django.contrib.auth import authenticate
from django import forms
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from .models import CustomUser, Address, Delivery, Payment, Product, Refund
from django.views.generic.edit import FormView
from django import forms


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            self.user = authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError("Incorrect username/password")


User = get_user_model()


class CustomLoginForm(AuthenticationForm):

    username = forms.CharField(label="Email/Username", max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        cleaned_data = super().clean()
        user = self.user_cache

        if user and user.is_staff:
            self.fields["username"].label = "Username"

        return cleaned_data


class UserCreationForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=("Enter the same password as above for verification."))
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number']
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class ProductSearchForm(forms.Form):
    query = forms.CharField(max_length=100, required=False, label='Search', widget=forms.TextInput(attrs={'placeholder':'Search product...', 'class':'form-control'}))

form = ProductSearchForm()
print(form.as_p())

class AddNewProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price','image', 'quantity_on_storage', 'category', 'brand', 'color', 'os', 'built_in_memory', 'screen_diagonal', 'battery_capacity', 'camera', 'processor', 'ram']

class ProductUpdateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'discount_price','image', 'quantity_on_storage', 'category', 'brand', 'color', 'os', 'built_in_memory', 'screen_diagonal', 'battery_capacity', 'camera', 'processor', 'ram']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['country', 'postal_code', 'city', 'street', 'house_number', 'phone_number']
        widgets = {
            'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter country'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter postal code'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter city'}),
            'street': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter street'}),
            'house_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter house number'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
        }

class DeliveryServiceForm(forms.ModelForm):
    class Meta:
        model = Delivery
        fields = ['delivery_service']
        widgets = {
            'delivery_service': forms.Select(attrs={'class': 'form-control'}),
        }


class ShippingForm(forms.Form):
    shipping_option = forms.ChoiceField(choices=[
        ('free', 'Free Regular Shipment'),
        ('fast', '200 CZK - Fastest Delivery'),
        ('schedule', 'Schedule Delivery')
    ], widget=forms.RadioSelect)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = []

# class RefundForm(forms.ModelForm):
#     class Meta:
#         model = Refund
#         fields = ['reason']


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = ['reason']
        widgets = {
            'reason': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter a reason'}),
        }
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.purchase = kwargs.pop('purchase', None)
        self.reason = kwargs.pop('reason', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        purchase = self.purchase
        payment = get_object_or_404(Payment, purchase=purchase)

        raise_an_error = False
        if not payment or payment.status != "completed":
            messages.error(self.request, "Payment not eligible for refund")
            raise_an_error = True
        if hasattr(purchase, 'refund'):
            messages.error(self.request, "Refund already requested")
            raise_an_error = True
        if raise_an_error:
            raise forms.ValidationError("Error occurred")
        return cleaned_data
