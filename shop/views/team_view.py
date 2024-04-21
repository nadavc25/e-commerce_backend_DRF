from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from shop.utils import generate_firebase_storage_url
from .serializers import TeamSerializer
from ..models import Team

class TeamView(APIView):
    # Helper method to get a team object by pk, no need to get 'pk' from kwargs here
    def get_object(self, pk):
        try:
            print("get object: ",  Team.objects.get(pk=pk).image)
            return Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # Adjusted get method to handle both list retrieval and single object retrieval
    def get(self, request, pk=None, format=None):
        if pk:
            team = self.get_object(pk)
            serializer = TeamSerializer(team)
        else:
            teams = Team.objects.all()
            serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("add team")
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
        serializer = TeamSerializer(data=updated_request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Adjusted put method, no significant changes needed here, just presented for completeness
    def put(self, request, pk, format=None):
        team = self.get_object(pk)
        if not isinstance(team, Response):  # Ensure team is not a Response object
            updated_data = request.data.copy()  # Copy the data to manipulate
            if 'image' in updated_data:
                # Convert image filename to URL
                updated_data['image'] = generate_firebase_storage_url(updated_data['image'])
            serializer = TeamSerializer(team, data=updated_data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return team  # Return the Response object from get_object if team not found

    # Your existing delete method (unchanged)
    def delete(self, request, pk, format=None):
        team = self.get_object(pk)
        if team is None:  # get_object already returns 404 response if not found
            return team  # This is a Response object with 404 status
        team.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
