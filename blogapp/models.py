from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    profile_pic=models.ImageField(upload_to="profilepics",null=True)
    bio=models.CharField(max_length=120)
    phone=models.CharField(max_length=15)
    date_of_birth=models.DateField(null=True)
    options=(
        ('male','male'),                         #one 'male' is the actual value and other one display value
        ('female','female'),
        ('other','other')
    )
    gender=models.CharField(max_length=12,choices=options,default='male')
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")             #(model relationship btw UserProfile-User models )


# on_delete=models.CASCADE-->if we are deleting the parent ,child occurence also should be removed.
# on_delete=models.CASCADE should be given in case of ForeignKey and OneToOneField
# 1:M Foreign key

class Blogs(models.Model):
    title=models.CharField(max_length=120)
    description=models.CharField(max_length=230)
    image=models.ImageField(upload_to="blogimages",null=True)
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="author")
    posted_date=models.DateTimeField(auto_now_add=True)
    liked_by=models.ManyToManyField(User)

    @property
    def get_like_count(self):
        like_count=self.liked_by.all().count()
        return like_count

    @property
    def get_liked_users(self):
        liked_users=self.liked_by.all()
        users=[user.username for user in liked_users]
        return users

    def __str__(self):
        return self.title


# related_name:it is used for parent to child referencing
# request.user will give that user
# request.user.users will give that child
# auto_now_add will give automatic system date and time

class Comments(models.Model):
    blog=models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment=models.CharField(max_length=160)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

# python manage.py createsuperuser
# superusers=[anj,django,python]
# password=[anj,django,python]

#deeps Password@123
#paru  Parus@123
#miakutty  Miaz@123

# fetching all comments related to a specific blog
# blog.Comments_set.all()


