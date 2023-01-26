from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from blogapp.forms import UserRegistrationForm,LoginForm,UserProfileForm,PasswordResetForm,BlogForm,CommentForm
from django.views.generic import View,CreateView,FormView,TemplateView,UpdateView
from django.contrib.auth import authenticate,login,logout
from blogapp.models import UserProfile,Blogs,Comments
from django.contrib import messages


# View
# creating a new object=> form,model,template_name =>CreateView
# fetching a specific object
# fetching all objects
# deleting an object
class SignUpView(CreateView):
    form_class=UserRegistrationForm
    template_name="registration.html"
    model=User
    success_url = reverse_lazy('signin')      #success_url should be mentioned during create and edit

    # def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{'form':form})
    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("")
    #     else:
    #         return render(request,self.template_name,{'form':form})
    #
class LoginView(FormView):
    model=User
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                print("success")
                return redirect("home")
            else:
                return render(request,self.template_name,{'form':form})

# FormView is for rendering a form in html page
# def get(self,request,*args,**kwargs):
    #     form=self.form_class()
    #     return render(request,self.template_name,{'form':form})
    # def post(self,request,*args,**kwargs):
    #     form=LoginForm(request.POST)
    #     if form.is_valid():
    #
    #         uname=form.cleaned_data.get("username")
    #         pwd=form.cleaned_data.get("password")
    #         user=authenticate(request,username=uname,password=pwd)  # authenticate() is used to check whether the username and password we given
    #                                                                 # are correct.If it is correct it will return a user object
    #         if user:
    #             login(request,user)                                 #login() is  to maintain the session
    #             print("success")                                    #request.user will give the name of the user logged in
    #             return redirect("emp-list")
    #         else:
    #             messages.error(request,"invalid credentials")
    #             return render(request,'login.html',{'form':form})

class IndexView(CreateView):
    model=Blogs
    form_class=BlogForm
    success_url = reverse_lazy("home")
    template_name="index.html"

    def form_valid(self, form):
        form.instance.author=self.request.user
        self.object=form.save()
        messages.success(self.request,"post has been saved")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):          # get_context_data :to add any extra context while going to client side
        context=super().get_context_data(**kwargs)
        blogs=Blogs.objects.all().order_by("-posted_date")   # '-' for descending order
        context["blogs"]=blogs
        comment_form=CommentForm()
        context["comment_form"]=comment_form
        return context

class CreateUserProfileView(CreateView):
    model=UserProfile
    template_name = "addprofile.html"
    form_class = UserProfileForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"profile has been created")
        self.object=form.save()
        return super().form_valid(form)

    # def post(self,request,*args,**kwargs):
    #     form=self.form_class(request.POST,files=request.FILES)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(self.request,"Profile has been created")
    #         return redirect("home")
    #     else:
    #         return render(request,self.template_name,{"form":form})

class ViewMyProfileView(TemplateView):
    template_name="viewprofile.html"

class PasswordResetView(FormView):
    template_name = "passwordreset.html"
    form_class = PasswordResetForm

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            oldpassword= form.cleaned_data.get('old_password')
            password1=form.cleaned_data.get('new_password')
            password2=form.cleaned_data.get('confirm_password')
            user=authenticate(request,username=request.user.username,password=oldpassword)  # "username" in user model
            if user:
                user.set_password(password2)
                user.save()
                messages.success(request,"password changed")
                return redirect("signin")
            else:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})

class ProfileUpdateView(UpdateView):
    model=UserProfile
    form_class=UserProfileForm
    template_name="profile-update.html"
    success_url=reverse_lazy("home")
    pk_url_kwarg = "user_id"                      # pk means primary key   ,this is to specifically update an object
    def form_valid(self,form):                    #form_valid is used for post activity, to add anything while going to database side
        messages.success(self.request,"Your profile has been successfully updated")
        self.object=form.save()
        return super().form_valid(form)

def add_comment(request,*args,**kwargs):
    if request.method=="POST":
        blog_id=kwargs.get("post_id")
        blog=Blogs.objects.get(id=blog_id)
        user=request.user
        comment=request.POST.get('comment')
        Comments.objects.create(blog=blog,comment=comment,user=user)
        messages.success(request,"comment has been posted")
        return redirect("home")

def add_like(request,*args,**kwargs):
    blog_id=kwargs.get('post_id')
    blog=Blogs.objects.get(id=blog_id)
    blog.liked_by.add(request.user)
    blog.save()
    return redirect("home")


