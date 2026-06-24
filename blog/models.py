from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
         return self.name

class Post(models.Model):
    title=models.CharField(max_length=255)
    content=models.TextField()
    image=models.ImageField(upload_to='post_images/',null=True,blank=True)
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    Created_at=models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,related_name='liked_post',blank=True)
    def __str__(self):
        return self.title


class Comment(models.Model): 
   post=models.ForeignKey(Post, on_delete=models.CASCADE)
   user=models.ForeignKey(User,on_delete=models.CASCADE)
   body=models.TextField()
   created_at=models.DateTimeField(auto_now_add=True)
   def __str__(self):
        return f"{self.user} - {self.post}"
   


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profile_pics/',default='default.jpg')


    def __str__(self):
        return self.user.username