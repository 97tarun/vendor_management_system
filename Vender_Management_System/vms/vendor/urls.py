from django.urls import path
from . import views

urlpatterns = [
    path('api/vendor/', views.VendorListCreate.as_view()),
    path('api/vendor/<int:pk>/', views.VendorRetrieveUpdateDestroy.as_view()),
    path('api/purchase_orders/', views.PurchaseOrderListCreate.as_view()),
    path('api/purchase_orders/<int:pk>/', views.PurchaseOrderRetrieveUpdateDestroy.as_view()),
    path('api/purchase_orders/<int:pk>/acknowledge/', views.AcknowledgePurchaseOrder.as_view()),
]
