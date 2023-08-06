from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [path("delete/<pk>/", views.DeleteAlertView.as_view(), name="delete")]
