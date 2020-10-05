from rest_framework import serializers
from .models import Post, Vote
#we need to create serializer for each model we're working 
#with so we need to import it. We use .models because we're
#importing it from the same folder.

class PostSerializer(serializers.ModelSerializer):
    #although there are different models, we're using the 
    #ModelSerializer because it makes it easy to translate
    #Django models into json objects.
    poster = serializers.ReadOnlyField(source='poster.username')
    poster_id = serializers.ReadOnlyField(source='poster.id')
    votes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','title','url','poster','poster_id','created','votes']
    #Serializers are basically a way that you can connect 
    #your fields and have some additional properties that
    #you can add later on. For eg. The 4 fields above
    #(except 'id' which is included in Django models by 
    #default)are what is included in the models but we will
    #need the vote count as well, which we can add via 
    #serializer.

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()

class VoteSerializer(serializers.ModelSerializer):
    #same as vote serializer
    class Meta:
        model = Vote
        #we change the model from Post to vote
        fields = ['id']
        #we only need the ID of the vote.