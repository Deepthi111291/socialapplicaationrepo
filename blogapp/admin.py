from django.contrib import admin
from blogapp.models import Blogs,Comments
# Register your models here.
admin.site.register(Blogs)          #Now admin can control Blogs
admin.site.register(Comments)       #Now admin can control Comments