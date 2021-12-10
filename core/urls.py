from django.urls import path, include

from core import views

urlpatterns = [
    path('latest-products/', views.ProductsListGuest.as_view()),
    path('latest-categories/', views.CategoriesListGuest.as_view()),
    
    path('products/search/', views.search),
    path('products/', views.ProductView.as_view()),
    path('products/shop/', views.ProductsList.as_view()),
    path('products/checkShared/', views.checkShared),
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
    path('orders/sold/', views.getSoldProducts),

    # DONE Create ShareView Class   # DONE Create ShareDetail Class
    path('shares/', views.ShareView.as_view()),
    path('shares/shop/', views.ShareList.as_view()),
    path('shares/<int:share_id>/', views.ShareDetail.as_view()),

    # DONE API for Profile
    path('profile/', views.ProfileView.as_view()),
    path('profile/<int:profile_id>/', views.ProfileDetail.as_view()),

    # DONE API for cash Deposit
    path('profile/deposit/', views.deposit),


]