from django.urls import path, include

from product import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('products/search/', views.search),
    path('products/', views.ProductView.as_view()),
    path('products/<int:product_id>/', views.ProductDetail.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('categories/<int:category_id>/', views.CategoryDetail.as_view()),
]