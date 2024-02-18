from django.db import models

# Create your models here.
from account.models import User
class BlogTable(models.Model):

              user = models.ForeignKey(User, on_delete=models.CASCADE)
              AuthorName = models.CharField(max_length=255,blank=True)
              Title = models.CharField(max_length=100, blank=True)
              Content = models.CharField(max_length=10000, blank=True)
              image = models.ImageField(null=True, blank=True, upload_to='blogimages/')


              def save(self, *args, **kwargs):
                            self.AuthorName = self.user.Fname +" "+ self.user.Lname
                            super().save(*args, **kwargs)
              def __str__(self):
                            return f"{self.AuthorName}, email= {self.user.email} => {self.Title}"

class LikeTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(BlogTable, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)


class CommentTable(models.Model):
              user = models.ForeignKey(User, on_delete=models.CASCADE)
              blog = models.ForeignKey(BlogTable, on_delete=models.CASCADE)
              comment = models.CharField(max_length=10000)
