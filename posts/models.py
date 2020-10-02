from django.db import models 
# this is imported by default
from django.contrib.auth.models import User 
#we need to import 'User' because we want to track who posted the link

class Post(models.Model):
    #create a class called post. Each model is a Python class that subclasses 
    # django.db.models.Model.
    title = models.CharField(max_length=100)
    #create a title of charfield built-in field, we define max length as 100.
    url = models.URLField()
    #create a title of urlfield built-in field.
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    #since we want to track who posted the link, we import User, and when the 
    #post is deleted on_delete=models.CASCADE tells Django to cascade the deleting effect 
    # i.e. continue deleting the dependent models as well. 
    created = models.DateTimeField(auto_now_add=True)
    #we add when the post was created and add the option to add the time as now.
    
    def __str__(self):
        return self.title    

    class Meta:
        ordering = ['-created']
        #we create this class to be able to display the posts; earliest first.

class Vote(models.Model):
    #we create this class so 1 user can only upvote once on a given post.  
    voter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
