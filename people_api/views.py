from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PeopleSerializer
from django.shortcuts import get_object_or_404

from .models import Person
# Create your views here.

# aws imports
import boto3
# adds a random string to end of image to ensure uniqueness 
import uuid
#environ
import os

class People(APIView):
   def get(self, request):
      people = Person.objects.all()
      data = PeopleSerializer(people, many=True).data
      return Response(data)
   
   def post(self, request):
            # stop database creation on image request to add to s3 instead of postgres
      photo_file = request.FILES.get('image', None)
      if photo_file:
         s3 = boto3.client('s3')
         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
         print(key)
         try:
            bucket = os.environ['S3_BUCKET']
             # send it off to S3
            s3.upload_fileobj(photo_file, bucket, key)
            # build the full url string to save in our DB
            #now convert url for postgres db
            newUrl = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            # get the data obj from our request
            data = request.data
            # add an image key to data obj for our new s3 image url
            data['image'] = newUrl
             # save our person data
            person = PeopleSerializer(data=data)
            if person.is_valid():
               person.save()
               return Response(person.data, status=status.HTTP_201_CREATED)
            else:
               return Response(person.errors, status=status.HTTP_400_BAD_REQUEST)
         except Exceptions as err:
            print('error with photo upload', err)
      return Response('upload error', status=status.HTTP_400_BAD_REQUEST)

class PeopleDetail(APIView):
   def get(self, request, pk):
      person = get_object_or_404(Person, pk=pk)
      data = PeopleSerializer(person).data
      return Response(data)
   
   def put(self, request, pk):
      # line grab 1 element from model or 404 - Not Found
      person = get_object_or_404(Person, pk=pk)
      updated = PeopleSerializer(person, data=request.data, partial=True)
      if updated.is_valid():
         updated.save()
         return Response(updated.data)
      else:
         return Response(updated.errors, status=status.HTTP_400_BAD_REQUEST)
   
   def delete(self, request, pk):
      person = get_object_or_404(Person, pk=pk)
      PeopleSerializer(person)
      person.delete()
      return Response(person, status.HTTP_204_NO_CONTENT)