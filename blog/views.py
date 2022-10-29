from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, BlogPostForm
from django.views.generic import UpdateView
from django.contrib import messages


def blogs(request):
    posts = BlogPost.objects.all()
    posts = BlogPost.objects.filter().order_by('-dateTime')
    return render(request, "blog.html", {'posts': posts})


def blogs_comments(request, slug):
    post = BlogPost.objects.filter(slug=slug).first()
    comments = Comment.objects.filter(blog=post)
    if request.method == "POST":
        user = request.user
        content = request.POST.get('content', '')
        blog_id = request.POST.get('blog_id', '')
        comment = Comment(user=user, content=content, blog=post)
        comment.save()
    return render(request, "blog_comments.html", {
        'post': post,
        'comments': comments
    })


def Delete_Blog_Post(request, slug):
    posts = BlogPost.objects.get(slug=slug)
    if request.method == "POST":
        posts.delete()
        return redirect('/')
    return render(request, 'delete_blog_post.html', {'posts': posts})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogPost.objects.filter(title__contains=searched)
        return render(request, "search.html", {
            'searched': searched,
            'blogs': blogs
        })
    else:
        return render(request, "search.html", {})


@login_required(login_url='/login')
def add_blogs(request):
    if request.method == "POST":
        form = BlogPostForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            blogpost = form.save(commit=False)
            blogpost.author = request.user
            blogpost.save()
            obj = form.instance
            alert = True
            return render(request, "add_blogs.html", {
                'obj': obj,
                'alert': alert
            })
    else:
        form = BlogPostForm()
    return render(request, "add_blogs.html", {'form': form})


class UpdatePostView(UpdateView):
    model = BlogPost
    template_name = 'edit_blog_post.html'
    fields = ['title', 'slug', 'content', 'image']


def user_profile(request, myid):
    post = BlogPost.objects.filter(id=myid)
    name = post[0].author
    user = User.objects.get(username = name)
    return render(request, "user_profile.html", {'i':user})


def profile_view(request):
    return render(request, "profile.html")


def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == "POST":
        form = ProfileForm(data=request.POST,
                           files=request.FILES,
                           instance=profile)
        if form.is_valid():
            form.save()
            alert = True
            return render(request, "edit_profile.html", {'alert': alert})
    else:
        form = ProfileForm(instance=profile)
    return render(request, "edit_profile.html", {'form': form})


def Register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        alert = {
            "username": request.GET.get('username', ''),
        }
        if User.objects.filter(username=request.POST['username']).exists():
            alert['username'] = "Username already exists"
            return render(request, "register.html", alert)

        user = User.objects.create_user(username, email, password1)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')
    return render(request, "register.html")


def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials")
        return render(request, 'login.html')
    return render(request, "login.html")


def Logout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')