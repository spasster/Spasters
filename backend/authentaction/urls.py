from django.contrib import admin
from django.urls import path
import authentaction.views as views 
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register/', views.register_user, name='auth_register'),
    path('login/', views.CustomAuth.as_view(), name='auth_login'),

    path('check_inn/', views.check_inn, name='check_inn'),

    path('user_info/', views.get_my_info, name='get_user_info'),
    path('seller_info/<int:user_id>/', views.get_user_info, name='get_seller_info'),

    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('reviews/', views.SellerReviewCreateView.as_view(), name='create-seller-review'),

    path('update_bio/', views.update_bio, name='update_bio'),
    path('update_avatar/', views.update_avatar, name='update_avatar'),

]