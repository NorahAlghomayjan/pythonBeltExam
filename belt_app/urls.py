from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index),
    path('main',views.main),
    path('dashboard',views.dashboard),
    path('login',views.login),
    path('register',views.register),
    path('saveUser/<int:id>',views.saveUser),
    path('wish_items/create',views.create),
    path('addItem/<int:id>',views.addItem),
    path('deleteItem/<int:id>',views.deleteItem),
    path('removeItem/<int:id>',views.removeItem),
    path('addtoWishList/<int:itemId>',views.addtoWishList),
    path('wish_items/<int:itemId>',views.item),
    path('logout/<int:id>',views.logout),
]