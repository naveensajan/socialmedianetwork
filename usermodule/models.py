from django.db import models

# Create your models here.
class User(models.Model):
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    email = models.EmailField(max_length=40, unique=True)
    password = models.CharField(max_length=70)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    description = models.CharField(max_length=160, blank=True, default="")
    profession = models.CharField(max_length=30, blank=True, default="")
    website = models.URLField(blank=True, default="")
    image = models.ImageField(upload_to="images" ,default="images/default.jpg")
    ustatus = models.IntegerField(default=0)

class Friend(models.Model):
    fid = models.ForeignKey('User',on_delete=models.CASCADE,related_name='fid')
    uid = models.ForeignKey('User',on_delete=models.CASCADE,related_name='uid')
    status =models.IntegerField()

class Post1(models.Model):
    uid = models.ForeignKey('User', on_delete=models.CASCADE)
    description=models.TextField()
    image = models.ImageField(upload_to="photos", default="")
    video= models.FileField(upload_to='videos', default="")
    cur_date=models.DateField()
    pcount = models.IntegerField(default=0)

class Likes(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    postId = models.ForeignKey('Post1', on_delete=models.CASCADE)

class Comment(models.Model):
    userId = models.ForeignKey('User', on_delete=models.CASCADE)
    postId = models.ForeignKey('Post1', on_delete=models.CASCADE)
    comment = models.TextField()

class Message(models.Model):
    body = models.TextField()
    msg_by = models.ForeignKey('User', on_delete=models.CASCADE,related_name='msg_by')
    msg_to = models.ForeignKey('User', on_delete=models.CASCADE,related_name='msg_to')
    msg_time = models.DateTimeField()