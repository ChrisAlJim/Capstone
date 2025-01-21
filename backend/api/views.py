from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer, IdeaSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Idea

# Create your views here.
class IdeaListCreate(generics.ListCreateAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Idea.objects.filter(thinker=user)
    
    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(thinker=self.request.user)
        else:
            print(serializer.errors)
        return 
    
class IdeaDelete(generics.DestroyAPIView):
    serializer_class = IdeaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Idea.objects.filter(thinker=user)

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]