from django.urls import path
from myapp.views import AdminMenuListView

urlpatterns = [
    path('', AdminMenuListView.as_view(), name='admin_menu'),
]