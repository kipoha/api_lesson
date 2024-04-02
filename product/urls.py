from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.CategoryListAPI.as_view()),
    path('categories/<int:id>/', views.CategoryDetailAPI.as_view()),
    path('products/', views.ProductListAPI.as_view()),
    # path('products/', views.product_list_view),
    path('products/<int:id>/', views.ProductDetailAPI.as_view()),
    path('reviews/', views.ReviewListAPI.as_view()),
    path('reviews/<int:id>/', views.ReviewDetailAPI.as_view()),
    path('products/reviews/', views.ProductReviewListAPI.as_view()),
]