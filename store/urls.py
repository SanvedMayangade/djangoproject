from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from store.controller import authview,cart,wishlist,checkout,order


urlpatterns = [
    path('', views.home, name='home'),
    path('collections', views.collections, name='collections'),
    path('collections/<str:slug>', views.collectionsview, name='collectionsview'),
    path('collections/<str:cate_slug>/<str:prod_slug>', views.productview, name='productview'),


    path('register/', authview.register, name='register'),
    path('login/', authview.loginpage, name='loginpage'),
    path('logout/', authview.logoutpage, name='logout'),
    
    path('add-to-cart', cart.addtocart, name='addtocart'),
    path('cart', cart.viewcart, name='cart'),
    path('update-cart', cart.updatecart, name='updatecart'),
    path('delete-cart-item', cart.deletecartitem, name='deletecartitem'),
    
    path('wishlist', wishlist.index, name='wishlist'),
    path('add-to-wishlist', wishlist.addtowishlist, name='addtowishlist'),
    path('delete-wishlist-item', wishlist.deletewishlistitem, name='deletewishlistitem'),

    path('checkout', checkout.index, name='checkout'),
    path('place-order', checkout.placeorder, name='placeorder'),
    path('proceed-to-pay', checkout.razorpaycheck, name='razorpaycheck'),
    
    path('my-orders', order.index, name='myorders'),
    path('view-order/<str:t_no>', order.vieworder, name='orderview'),

    path('product-list', views.productlistajax),
    path('category-list',views.categorylistajax),
    # path('searchcategory',views.searchcategory, name="searchcategory"),
    path('searchproducts', views.searchproducts, name="searchproducts"),

    #foget passwordd urls
    path('password_reset/',auth_views.PasswordResetView.as_view(),name="password_reset"),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
    # path('accounts/',include('django.contrib.auth.urls')),
]