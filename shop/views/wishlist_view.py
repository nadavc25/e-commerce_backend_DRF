from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from .serializers import WishlistSerializer, WishlistItemSerializer
from ..models import Wishlist, WishlistItem

@permission_classes([IsAuthenticated])
class WishlistView(APIView):
    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data)

    def post(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        item_serializer = WishlistItemSerializer(data=request.data)
        if item_serializer.is_valid():
            item_serializer.save(wishlist=wishlist)
            return Response(item_serializer.data, status=status.HTTP_201_CREATED)
        return Response(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        wishlist = get_object_or_404(Wishlist, user=request.user)
        item = get_object_or_404(WishlistItem, pk=pk, wishlist=wishlist)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
