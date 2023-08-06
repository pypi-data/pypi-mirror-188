from django.urls import path
from medux.preferences import views

app_name = "preferences"

urlpatterns = [
    path("", views.PreferencesView.as_view(), name="index"),
]
