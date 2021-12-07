from django.urls import path, include

from core import views

urlpatterns = [
    path('latest-products/', views.LatestProductsList.as_view()),
    path('latest-categories/', views.LatestCategoriesList.as_view()),
    path('products/search/', views.search),
    path('products/', views.ProductView.as_view()),
    path('products/<int:product_id>/', views.ProductDetail.as_view()),
    path('categories/', views.CategoryView.as_view()),
    path('categories/<int:category_id>/', views.CategoryDetail.as_view()),
    path('transactions/', views.TransactionView.as_view()),
    path('transactions/<int:transaction_id>/', views.TransactionDetail.as_view()),
    
    # TODO Create GiftView Class

    # TODO Create GiftDetail Class

    # TODO Create OrderView Class

    # TODO Create OrderDetail Class

    # TODO Create ShareView Class

    # TODO Create ShareDetail Class

    # TODO API for cash Deposit

    # TODO API for Profile

]