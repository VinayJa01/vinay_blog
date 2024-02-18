from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from account.models import *
from xml.dom import ValidationErr
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class BlogUploadSerializers(serializers.ModelSerializer):


    class Meta:
        model = BlogTable
        fields = ['AuthorName','Title', 'Content', 'image']

    
class AllBlogViewSerializers(serializers.ModelSerializer):


    class Meta:
        model = BlogTable
        fields = ['id','AuthorName','Title', 'Content', 'image']

    
class LikeViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = LikeTable
        fields = "__all__"

    
class CommentBlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = CommentTable
        fields = "__all__"

class CommentBlogUserSerializers(serializers.ModelSerializer):
    user_Fname = serializers.CharField(source='user.Fname', read_only=True)
    user_Lname = serializers.CharField(source='user.Lname', read_only=True)

    class Meta:
        model = CommentTable
        fields = ['user_Fname', 'user_Lname','comment']
