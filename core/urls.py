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
    
    # DONE Create GiftView Class     # DONE Create GiftDetail Class
    path('gifts/', views.GiftView.as_view()),
    path('gifts/<int:gift_id>/', views.GiftDetail.as_view()),
    # DONE Create OrderView Class   # DONE Create OrderDetail Class

    path('orders/', views.OrderView.as_view()),
    path('orders/<int:order_id>/', views.OrderDetail.as_view()),

    # DONE Create ShareView Class   # DONE Create ShareDetail Class
    path('shares/', views.ShareView.as_view()),
    path('shares/<int:share_id>/', views.ShareDetail.as_view()),

    path('profile/', views.ProfileView.as_view()),
    path('profile/<int:profile_id>/', views.ProfileDetail.as_view()),



    

    # TODO API for cash Deposit

    # TODO API for Profile

]