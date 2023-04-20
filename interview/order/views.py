from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer


# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(generics.UpdateAPIView):
    """
    Updates an order object to set is_active to False and nothing else.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def update(self, request: Request, *args, **kwargs) -> Response:
        """Hard-coded to allow only the deactivation of the order."""
        order: Order = self.get_object()
        Order.deactivate(pk=order.pk)
        # The deactivate method does not update the in-memory instance, so update that before serializing.
        order: Order = self.get_object()
        serializer: OrderSerializer = self.get_serializer(order)
        return Response(serializer.data)
