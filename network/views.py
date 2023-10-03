from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Following, Like

import json


def index(request):
    allPosts = Post.objects.all().order_by("id").reverse()

    # For paginator
    paginator = Paginator(allPosts, 10)
    getPageNumber = request.GET.get('page')
    posts_on_page = paginator.get_page(getPageNumber)

    # For getting all the likes and work with them
    likes = Like.objects.all()

    yourLike = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                yourLike.append(like.post.id)
    except:
        yourLike = []

    return render(request, "network/index.html", {
        "allPosts": allPosts,
        "posts_on_page": posts_on_page,
        "yourLike": yourLike
    })


def unlike(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    removeLike = Like.objects.filter(user=user, post=post)
    removeLike.delete()

    # Update like counter
    likes_count = Like.objects.filter(post=post).count()
    post.likes = likes_count
    post.save()

    return JsonResponse({"message": "Your like was removed!", "likes": likes_count})


def give_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(pk=request.user.id)
    clickLike = Like(user=user, post=post)
    clickLike.save()

    likes_count = Like.objects.filter(post=post).count()
    post.likes = likes_count
    post.save()
    return JsonResponse({"message": "You liked this post!", "likes": likes_count})


def editPost(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.contenido = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Changes saved!", "data": data["content"] })

def newPost(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(contenido=content, usuario=user)
        post.save()
        return HttpResponseRedirect(reverse(index))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def profile_page(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(usuario=user).order_by("id").reverse()

    following = Following.objects.filter(user=user)
    followers = Following.objects.filter(followed=user)

    try:
        checkFollowing = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(checkFollowing) != 0:
            already_following = True
        else:
            already_following = False
    except:
        already_following = False

    # For paginator
    paginator = Paginator(allPosts, 10)
    getPageNumber = request.GET.get('page')
    posts_on_page = paginator.get_page(getPageNumber)

    # For getting all the likes and work with them
    likes = Like.objects.all()

    yourLike = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                yourLike.append(like.post.id)
    except:
        yourLike = []

    return render(request, "network/profile_page.html", {
        "allPosts": allPosts,
        "posts_on_page": posts_on_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "already_following": already_following,
        "user_profilepage": user,
        "yourLike": yourLike
    })


def follow(request):
    userdoesfollow = request.POST['userdoesfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowInfo = User.objects.get(username=userdoesfollow)
    foll = Following(user=currentUser, followed=userfollowInfo)
    foll.save()
    user_id = userfollowInfo.id 
    return HttpResponseRedirect(reverse(profile_page, kwargs={'user_id': user_id}))


def unfollow(request):
    userdoesfollow = request.POST['userdoesfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowInfo = User.objects.get(username=userdoesfollow)
    foll = Following.objects.get(user=currentUser, followed=userfollowInfo)
    foll.delete()
    user_id = userfollowInfo.id 
    return HttpResponseRedirect(reverse(profile_page, kwargs={'user_id': user_id}))


def follows(request):
    currentUser = User.objects.get(pk=request.user.id)
    following = Following.objects.filter(user=currentUser)
    allPosts = Post.objects.all().order_by("id").reverse()
    post_of_followed = []

    for post in allPosts:
        for person in following:
            if person.followed == post.usuario:
                post_of_followed.append(post)

    # For paginator
    paginator = Paginator(post_of_followed, 10)
    getPageNumber = request.GET.get('page')
    posts_on_page = paginator.get_page(getPageNumber)

     # For getting all the likes and work with them
    likes = Like.objects.all()

    yourLike = []
    try:
        for like in likes:
            if like.user.id == request.user.id:
                yourLike.append(like.post.id)
    except:
        yourLike = []

    return render(request, "network/follows.html", {
        "posts_on_page": posts_on_page,
        "yourLike": yourLike
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
