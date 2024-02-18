# from django.contrib import admin
# from django.urls import path,include



# urlpatterns = [
#      path('/blogupload', Upload_Blog.as_view(), name="Upload Blog Endpoint")
# ]


from django.contrib import admin
from django.urls import path,include
from blog.views import *
urlpatterns = [
    path('uploadblog/', Blog.as_view(), name="Upload/View Blog Endpoint"),
    path('', AllBlog.as_view(), name="Upload/View Blog Endpoint"),
    path('like/',LikeBlogView.as_view(), name="Like blog post"),
    path('likecount/',GETLikeCount.as_view(), name="Get like count"),
    path('comment/',CommentBlogView.as_view(), name="Comment blog")

  
   
   
]
