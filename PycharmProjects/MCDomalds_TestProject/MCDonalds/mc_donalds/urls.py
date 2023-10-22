from django.urls import path
from .views import ProductsList, ProductsDetail, ProductCreate, ProductUpdate, ProductDelete

urlpatterns = [
    path('', ProductsList.as_view()),
    path('<int:pk>', ProductsDetail.as_view(), name='product_detail'),
    path('create/', ProductCreate.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDelete.as_view(), name='product_delete')
]
