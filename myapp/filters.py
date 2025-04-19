import django_filters
from .models import Product, Category, Brand, Color, OS

class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all())
    color = django_filters.ModelChoiceFilter(queryset=Color.objects.all())
    os = django_filters.ModelChoiceFilter(queryset=OS.objects.all())
    built_in_memory = django_filters.NumberFilter(field_name="built_in_memory")
    screen_diagonal = django_filters.NumberFilter(field_name="screen_diagonal")
    battery_capacity = django_filters.NumberFilter(field_name="battery_capacity")
    camera = django_filters.NumberFilter(field_name="camera")
    processor = django_filters.CharFilter(field_name="processor", lookup_expr="icontains")
    ram = django_filters.NumberFilter(field_name="ram")

    class Meta:
        model = Product
        fields = [
            'price_min', 'price_max', 'category', 'brand', 'color', 'os',
            'built_in_memory', 'screen_diagonal', 'battery_capacity', 'camera',
            'processor', 'ram'
        ]
