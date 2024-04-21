from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop.utils import generate_firebase_storage_url
from .serializers import LeagueSerializer  # Make sure to create a serializer for the League model
from ..models import League

class LeagueView(APIView):
    # Helper method to get a league object by pk
    def get_object(self, pk):
        try:
            return League.objects.get(pk=pk)
        except League.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Method to handle both list retrieval and single object retrieval
    def get(self, request, pk=None, format=None):
        if pk:
            league = self.get_object(pk)
            serializer = LeagueSerializer(league)
        else:
            leagues = League.objects.all()
            serializer = LeagueSerializer(leagues, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("add league")
        # Make a mutable copy of the request data
        updated_request_data = request.data.copy()
        
        # Check if 'image' is in the request data and convert it
        if 'image' in updated_request_data:
            image_filename = updated_request_data['image']
            # Use your function to generate a URL from the filename
            image_url = generate_firebase_storage_url(image_filename)
            # Update the request data with the generated URL
            updated_request_data['image'] = image_url

        # Now proceed with the updated request data
        serializer = LeagueSerializer(data=updated_request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Method to handle league updates
    def put(self, request, pk, format=None):
        team = self.get_object(pk)
        if not isinstance(team, Response):  # Ensure team is not a Response object
            updated_data = request.data.copy()  # Copy the data to manipulate
            if 'image' in updated_data:
                # Convert image filename to URL
                updated_data['image'] = generate_firebase_storage_url(updated_data['image'])
            serializer = LeagueSerializer(team, data=updated_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return team  # Return the Response object from get_object if team not found

    # Method to handle league deletion
    def delete(self, request, pk, format=None):
        league = self.get_object(pk)
        if isinstance(league, Response):  # Check if get_object returned a 404 Response
            return league
        league.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
