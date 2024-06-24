# shop\views\order_views.py
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import OrderSerializer, OrderDetailsSerializer
from ..models import Order, OrderDetails
from ..utils import send_order_notification 

@permission_classes([IsAuthenticated])
class OrderView(APIView):
    def post(self, request):
        serializer = OrderSerializer(data=request.data, context={'request': request})  # Include 'request' in the context
        if serializer.is_valid():
            order = serializer.save()
            
            # Create OrderDetails objects for each item in the list
            for item in request.data["items"]:
                item['order'] = order.id  # Assuming there's a foreign key to Order in OrderDetails
                serializerDt = OrderDetailsSerializer(data=item)
                if serializerDt.is_valid():
                    serializerDt.save()
                else:
                    return Response(serializerDt.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Calculate and update the total price
            order.total_price = order.calculate_total_price()
            order.save()

            # Send email notification
            send_order_notification(order)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        order = request.user.order_set.all().prefetch_related('items')  # Prefetch related items
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)
