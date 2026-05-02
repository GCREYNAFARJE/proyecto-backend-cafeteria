from django.views.generic import DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect, get_object_or_404

from .models import Order
from .forms import OrderProductForm


# Vista para mostrar la orden activa del usuario
class MyOrderView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = "orders/my_order.html"
    context_object_name = "order"

    def get_object(self, queryset=None):
        order = Order.objects.filter(is_active=True, user=self.request.user).first()
        if not order:
            # Si no hay orden activa, crea una nueva automáticamente
            order = Order.objects.create(user=self.request.user, is_active=True)
        return order


# Vista para agregar productos a la orden
class CreateOrderProductView(LoginRequiredMixin, CreateView):
    template_name = "orders/create_order_product.html"
    form_class = OrderProductForm
    success_url = reverse_lazy("my_order")

    def form_valid(self, form):
        # Obtiene o crea la orden activa del usuario
        order, _ = Order.objects.get_or_create(
            is_active=True,
            user=self.request.user,
        )
        form.instance.order = order
        form.instance.quantity = 1
        form.save()
        return super().form_valid(form)


# Vista para eliminar pedido
class DeleteOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user, is_active=True)
        order.delete()
        # Después de eliminar, redirige a crear uno nuevo
        return redirect("new_order")


# Vista para crear un nuevo pedido y redirigir al catálogo
class NewOrderView(LoginRequiredMixin, View):
    def get(self, request):
        # Cierra cualquier orden activa
        Order.objects.filter(user=request.user, is_active=True).update(is_active=False)
        # Crea una nueva orden vacía
        Order.objects.create(user=request.user, is_active=True)
        # Redirige al catálogo de productos
        return redirect("list_product")
