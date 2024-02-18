from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(BlogTable)
admin.site.register(LikeTable)
admin.site.register(CommentTable)
