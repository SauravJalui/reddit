from django.shortcuts import render
from rest_framework import generics,permissions
from .models import Post
from .serializers import PostSerializer

#we want this API to be able to show all the posts
#that are saved in the database.
class PostList(generics.ListCreateAPIView):
    #Here we are making a class based view and we
    #are listing out information using ListAPIView
    queryset = Post.objects.all()
    #now we need to know what serializer we will be
    #using for this particular view
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        #it's very important that we use the same
        #name for the function as it is special
        #function that gets called before the 
        #data is saved in the db.
        serializer.save(poster=self.request.user)
        #this sets the poster as the user itself 
        #while saving the data.