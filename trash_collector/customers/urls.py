from django.urls import path

from . import views

app_name = "customers"
urlpatterns = [
    path('', views.index, name="index"),
    path('new/', views.create, name="create"),
    path('suspend/<int:pk>', views.suspend_service, name="suspend"),
    path('one_time/<int:pk>', views.one_time_pickup, name="one_time"),
    path('edit_profile/<int:pk>', views.edit_profile, name="edit_profile"),
]
