from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import *
from account.models import *
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .serializers import *
from account.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
class Blog(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        print("Inside")
        print(request.headers)
        user_id = request.headers.get('userid')

        if user_id is None:
            return Response({'message': 'User ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        
        serializer = BlogUploadSerializers(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(user=user)
            return Response({'message': 'Blog uploaded Successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, format=None):
       
        user_id = request.headers.get('userid')

        if user_id is None:
            return Response({'message': 'User ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        blog_id = request.headers.get('blogid')
        try:
            requestedblog = BlogTable.objects.get(id = blog_id)
            serializer = BlogUploadSerializers(requestedblog, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user)
                return Response({'message': 'Blog updated Successfully'}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, format=None):
        
        user_id = request.headers.get('userid')
        if user_id is None:
            return Response({'message': 'User ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)


        blog_id = request.headers.get('blogid')
        if blog_id is None:
            return Response({'message': 'Blog ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requestedblog = get_object_or_404(BlogTable,id = blog_id)
            requestedblog.delete()
            return Response({'message': 'Blog deleted Successfully'}, status=status.HTTP_404_NOT_FOUND)

            
        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request, format=None):  
        try:
            if user_id is None:
                return Response({'message': 'User ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

            blog_id = request.headers.get('blogid')
            if blog_id:
                requestedblog = BlogTable.objects.get(id = blog_id)
                serializer = AllBlogViewSerializers(requestedblog)
                return Response(serializer.data, status=status.HTTP_200_OK)



            allBlogs = BlogTable.objects.filter(user=user)

            serializer = AllBlogViewSerializers( allBlogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)


    



 


class AllBlog(APIView):
    def get(self, request, format=None):
        try:
            blog_id = request.headers.get('blogid')
            if blog_id:
                requestedblog = BlogTable.objects.get(id = blog_id)
                serializer = AllBlogViewSerializers(requestedblog)
                return Response(serializer.data, status=status.HTTP_200_OK)



            allBlogs = BlogTable.objects.all()

            serializer = AllBlogViewSerializers( allBlogs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)
    

class LikeBlogView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        user_id = request.headers.get('userid')
        if user_id is None:
            return Response({'message': 'User ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        blog_id = request.headers.get('blogid')
        if blog_id is None:
            return Response({'message': 'Blog ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requestedblog = get_object_or_404(BlogTable, id=blog_id)
        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)

        likeval = request.data.get("like")
        if likeval:
            obj = LikeTable.objects.filter(blog=requestedblog, user=user).first()

            if obj:
               
                serializer = LikeViewSerializers(obj, data={'like': likeval}, partial=True)
            else:
               
                serializer = LikeViewSerializers(data={'like': likeval, 'user': user.id, 'blog': requestedblog.id})

            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, blog=requestedblog)
                if likeval == "True":
                    ans = "Liked"
                else:
                    ans = "Disliked"
                message = f"{ans} Successfully"
                return Response({'message': message}, status=status.HTTP_200_OK)



        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        user_id = request.headers.get('userid')
        if user_id is None:
            return Response({'message': 'User ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        blog_id = request.headers.get('blogid')
        if blog_id is None:
            return Response({'message': 'Blog ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requestedblog = get_object_or_404(BlogTable, id=blog_id)
        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)

        obj = LikeTable.objects.filter(blog=requestedblog, user=user).first()

        if obj:
               
            serializer = LikeViewSerializers(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            likeval = "False"
            serializer = LikeViewSerializers(data={'like': likeval, 'user': user.id, 'blog': requestedblog.id})
         
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=user, blog=requestedblog)

            return Response(serializer.data, status=status.HTTP_200_OK)



class GETLikeCount(APIView):
    def get(self, request, format=None):
        blog_id = request.headers.get('blogid')
        if blog_id is None:
            return Response({'message': 'Blog ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requestedblog = get_object_or_404(BlogTable, id=blog_id)
        except BlogTable.DoesNotExist:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)

        obj = LikeTable.objects.filter(blog=requestedblog,like=True).count()
        
              
        return Response({'message':obj})



class CommentBlogView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = self.request.user

        blog_id = request.headers.get('blogid')
        if blog_id is None:
            return Response({'message': 'Blog ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        requestedblog = get_object_or_404(BlogTable, id=blog_id)

        comment_val = request.data.get("comment")
        if not comment_val:
            return Response({'message': 'Comment value is required.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CommentBlogSerializers(data={'comment': comment_val, 'user': user.id, 'blog': requestedblog.id})
        if serializer.is_valid():
            serializer.save(user=user, blog=requestedblog)
            return Response({'message': serializer.data['comment']}, status=status.HTTP_200_OK)
        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        

        blog_id = request.headers.get('blogid')
        if blog_id is None:
            return Response({'message': 'Blog ID not provided in headers.'}, status=status.HTTP_400_BAD_REQUEST)

        requestedblog = get_object_or_404(BlogTable, id=blog_id)

        if requestedblog is not None:
            obj = CommentTable.objects.filter(blog=requestedblog)
            serializer = CommentBlogUserSerializers(obj, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Blog not found.'}, status=status.HTTP_404_NOT_FOUND)

            
