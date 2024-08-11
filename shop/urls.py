# shop\urls.py
from django.urls import path

from shop.views import auth_views
from .views import (
    cart_view, order_views, patch_view, product_views,
    review_view, team_view, user_views, wishlist_view, League_View
)
from . import main_views 
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('', main_views.index, name='home'),
    path('user/', user_views.UserDetailView.as_view(), name='user-detail'),
    path('register/', main_views.register),
    path('login/', main_views.MyTokenObtainPairView.as_view()),
    path('logout/', main_views.Logout.as_view(), name='logout'),
    path('products/', product_views.ProductView.as_view(), name='product-list'),
    path('products/<int:pk>/', product_views.ProductView.as_view(), name='product_detail'),
    path('cart/', cart_view.CartView.as_view(), name='cart_list'),
    path('wishlist/', wishlist_view.WishlistView.as_view(), name='wishlist_list'),
    path('orders/', order_views.OrderView.as_view(), name='order_list'),
    path('orders/<int:pk>/', order_views.OrderView.as_view(), name='order_detail'),
    path('teams/', team_view.TeamView.as_view(), name='team-list'),
    path('teams/<int:pk>/', team_view.TeamView.as_view(), name='team-detail'),  
    path('leagues/', League_View.LeagueView.as_view(), name='league_list'),
    path('leagues/<int:pk>/', League_View.LeagueView.as_view(), name='get_League'),
    path('patches/', patch_view.PatchView.as_view(), name='patch_list'),
    path('patches/<int:pk>/', patch_view.PatchView.as_view(), name='patch_detail'),
    path('reviews/', review_view.ReviewView.as_view(), name='review_list'),
    path('reviews/<int:pk>/', review_view.ReviewView.as_view(), name='review_detail'),
    # Add more patterns for other views as needed
    path('auth/google/', auth_views.GoogleLoginAPIView.as_view(), name='google-login'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', main_views.search_products, name='search-products'),

]
