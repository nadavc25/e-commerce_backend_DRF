from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import FieldError
from shop.utils import generate_firebase_storage_url
from .serializers import ProductSerializer
from ..models import League, Product, SizeTypeCategory, SportType, Team

class ProductView(APIView):
    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        filter_params = self.request.query_params
        print("Filter Params:", filter_params)

        for filter_type, filter_value in filter_params.items():
            if filter_type == 'available':
                continue  # Skip the 'available' filter as it's already applied
            
            try:
                field = Product._meta.get_field(filter_type)
                if field.get_internal_type() == 'ForeignKey':
                    # Map string filter value to the ForeignKey ID
                    related_model = field.related_model
                    related_obj = get_object_or_404(related_model, name__iexact=filter_value)
                    filter_kwargs = {f'{filter_type}__id': related_obj.id}
                else:
                    filter_kwargs = {f'{filter_type}__iexact': filter_value}
                queryset = queryset.filter(**filter_kwargs)
            except FieldError:
                print(f"FieldError: Unsupported field '{filter_type}'")
                queryset = Product.objects.none()  # Return empty queryset if field is not valid
            except related_model.DoesNotExist:
                print(f"Error: Related object with name '{filter_value}' does not exist.")
                queryset = Product.objects.none()  # Return empty queryset if related object does not exist

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
