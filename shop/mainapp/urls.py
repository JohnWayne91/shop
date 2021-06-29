from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import *
urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-amount/<str:slug>/', ChangeProductAmountView.as_view(), name='change_amount'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('payed-online-order/', PayedOnlineOrderView.as_view(), name='payed_online'),
    path('sign-in/', SignInUser.as_view(), name='sign_in'),
    path('sign-out/', LogoutView.as_view(next_page='/sign-in/'), name='sign_out'),
    path('sign-up/', RegisterUser.as_view(), name='sign_up'),
    path('profile/', ProfileView.as_view(), name='profile')

]

