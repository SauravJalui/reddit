from django.shortcuts import render
from rest_framework import generics,permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Vote
from .serializers import PostSerializer, VoteSerializer

# we want this API to be able to show all the posts that are saved in the database.
class PostList(generics.ListCreateAPIView):
    # Here we are making a class based view and we are listing out information 
    # using ListAPIView
    queryset = Post.objects.all()
    #now we need to know what serializer we will be using for this particular view
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        #it's very important that we use the same name for the function as it is 
        # special function that gets called before the data is saved in the db.
        serializer.save(poster=self.request.user)
        #this sets the poster as the user itself while saving the data.

class PostRetrieveDestroy(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def delete(self, request, *args, **kwargs):
        post = Post.objects.filter(pk=kwargs['pk'],poster=self.request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('You do not have access to delete this post')

class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    #This is only to create new votes and list all upvotes.
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    #we remove the readonly as we want the person to be logged in to upvote a post.

    def get_queryset(self):
        #this is because we are looking for a particular user and a particular post
        user = self.request.user
        #the user is the one that makes the request
        post = Post.objects.get(pk=self.kwargs['pk'])
        #the primary key(pk) would be whatever was passed in the url. 
        # so if it is the 1st post the pk would be 1
        return Vote.objects.filter(voter=user, post=post)
        #this would return the user that is making the request and the post that 
        #we imported from the models
    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already upvoted this')
        serializer.save(voter=self.request.user, post = Post.objects.get(pk=self.kwargs['pk']))
        #this sets the poster as the user itself while saving the data.

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            #we first check if the post and vote exists.
            self.get_queryset().delete()
            #we can only delete if it exists.
            return Response(status=status.HTTP_204_NO_CONTENT)
            #we return "NO CONTENT" status.
        else:
            raise ValidationError('You did not vote for this post yet')
            #if the post does not exist we raise a validation error.