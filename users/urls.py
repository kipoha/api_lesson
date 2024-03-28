from django.urls import path
from users import views

urlpatterns = [
    path('registration/', views.reg_user_api_view),
    path('login/', views.auth_user_api_view),
    path('confirm/', views.confirm_user_api_view)
]