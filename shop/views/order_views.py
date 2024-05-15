# shop\views\order_views.py
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import OrderSerializer, OrderDetailsSerializer
from ..models import Order, OrderDetails

@permission_classes([IsAuthenticated])
class OrderView(APIView):
    def post(self, request):
        with transaction.atomic():
            serializer = OrderSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                order = serializer.save()

                # Assuming 'items' is a list of dictionaries representing order items
                items_data = request.data.get("items", [])
                for item_data in items_data:
                    item_data['order'] = order.id
                    item_serializer = OrderDetailsSerializer(data=item_data)
                    if item_serializer.is_valid():
                        item_serializer.save()
                    else:
                        # If any item is invalid, rollback the whole transaction
                        transaction.set_rollback(True)
                        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # Fetch orders for the logged-in user
        orders = request.user.order_set.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
