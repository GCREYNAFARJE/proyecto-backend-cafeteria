from django.urls import path
from .views import MyOrderView, CreateOrderProductView, DeleteOrderView, NewOrderView

urlpatterns = [
    path("mi-orden", MyOrderView.as_view(), name="my_order"),
    path("agregar-producto", CreateOrderProductView.as_view(), name="add_product"),
    path("eliminar/<int:pk>/", DeleteOrderView.as_view(), name="delete_order"),
    path("nuevo-pedido/", NewOrderView.as_view(), name="new_order"),
]
