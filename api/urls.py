from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .import views
router = DefaultRouter()
router.register('product', views.ProductViewSet)
router.register('category', views.CategoryViewSet)
router.register('cart', views.CartViewSet)
router.register('order', views.OrderViewSet)
router.register('cartitem', views.CartItemViewSet)
urlpatterns = [path('register/', views.register),
               path('login/', views.login),
               path('checkout/', views.checkout),
               path('', include(router.urls))

               ]
