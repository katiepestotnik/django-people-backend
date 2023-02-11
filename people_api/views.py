from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PeopleSerializer
from django.shortcuts import get_object_or_404

from .models import Person
# Create your views here.


class People(APIView):
   def get(self, request):
    people = Person.objects.all()
    data = PeopleSerializer(people, many=True).data
    return Response(data)
   
   def post(self, request):
      person = PeopleSerializer(data=request.data)
      if person.is_valid():
         person.save()
         return Response(person.data, status=status.HTTP_201_CREATED)
      else:
         return Response(person.errors, status=status.HTTP_400_BAD_REQUEST)

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