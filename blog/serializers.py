from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category,Post,Comment,Profile


#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
      model=User
      fields=['id','username','email']


#Category serializer
class CategorySerializer(serializers.ModelSerializer):
   class Meta:
      model=Category
      fields=  ['id','name']


 #post serializer
class PostSerializer(serializers.ModelSerializer):
   #read only display field
   author=UserSerializer(read_only=True)
   category=CategorySerializer(read_only=True)

   #write only fields(for creating and updating via id)
   author_id=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),source='author',write_only=True)

   category_id=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(),source='category',write_only=True) 

   total_likes=serializers.SerializerMethodField()

   class Meta:
      model=Post
      fields=[
         'id',
         'title',
         'content',
         'author',
         'author_id',
         'category',
         'category_id',
         'Created_at',
         'likes',
         'total_likes'
         
      ]
      read_only_fields=['likes','Created_at']

   def get_total_likes(self,obj):
         return obj.likes.count()
   


   #comment serializers
class CommentSerializers(serializers.ModelSerializer):
   user=UserSerializer(read_only=True)
   post=serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())

   class Meta:
      model=Comment
      fields=['id','post','user','body','created_at']
      read_only_fields=['created_at']   


#profile serializer
class ProfileSerializer(serializers.ModelSerializer) :
   user=UserSerializer(read_only=True)


   class Meta:
      model=Profile
      fields=['id','user','image']    
