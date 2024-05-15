# shop\views\product_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from shop.utils import generate_firebase_storage_url
from .serializers import ProductSerializer
from ..models import League, Product, SportType, Team

class ProductView(APIView):
    def get_queryset(self):
        queryset = Product.objects.filter(available=True)  # Only fetch products that are marked as available
        league_slug = self.request.query_params.get('league')
        sport_type_slug = self.request.query_params.get('sport_type')
        team_slug = self.request.query_params.get('team')

        
        # Apply filters if they are in query parameters
        if league_slug:
            print(league_slug)
            league = get_object_or_404(League, name=league_slug)
            print("league", league)
            queryset = queryset.filter(league=league)
        if sport_type_slug:
            print(sport_type_slug)
            sport_type = get_object_or_404(SportType, name=sport_type_slug)
            queryset = queryset.filter(sport_type=sport_type)
        if team_slug:
            team = get_object_or_404(Team, name=team_slug)
            queryset = queryset.filter(team=team)

        return queryset

    def get(self, request, pk=None, format=None):
        """
        GET method to list products or retrieve a single product.
        """
        if pk:
            # Retrieve a single product by pk (id)
            product = get_object_or_404(Product, pk=pk)
            serializer = ProductSerializer(product)
        else:
            # List all products or apply filters
            products = self.get_queryset()
            serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        if not isinstance(product, Response):  # Ensure team is not a Response object
            updated_data = request.data.copy()  # Copy the data to manipulate
            if 'main_image_url' in updated_data:
                # Convert image filename to URL
                updated_data['main_image_url'] = generate_firebase_storage_url(updated_data['main_image_url'])
            serializer = ProductSerializer(product, data=updated_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return product  # Return the Response object from get_object if team not found

    def delete(self, request, product_id, format=None):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
