from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ..models import Patch
from .serializers import PatchSerializer

# @permission_classes([IsAuthenticated])
class PatchView(APIView):
    def get(self, request, format=None):
        patches = Patch.objects.all()
        serializer = PatchSerializer(patches, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        patch = get_object_or_404(Patch, pk=pk)
        serializer = PatchSerializer(patch, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        patch = get_object_or_404(Patch, pk=pk)
        patch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
