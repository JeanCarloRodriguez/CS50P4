import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage 

from .models import User, Post, Follow


def index(request):
    if request.user.is_authenticated:
        return feed(request, "all")
    else:
        return login_view(request)

def followings_view(request):
    if request.user.is_authenticated:
        return render(request, "network/followings.html")
    else:
        return login_view(request)

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

@login_required(login_url='/login', redirect_field_name='')
def profile_view(request, username):
    user = User.objects.get(username=username)
    posts = user.posts.all().order_by("-timestamp")

    paginator = Paginator(posts, 10)
    page_num = request.GET.get("page", 1)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    return render(request, "network/profile.html", { 
        "profile_user_id": user.id,
        "profile_user_name": user.username,
        "posts": page
    })

def feed(request, option):
    if option.lower() == "all":
        posts = Post.objects.all().order_by("-timestamp")
    elif option.lower() == "followings":
        followings = request.user.serialize()["followings"]
        posts = Post.objects.filter(user__pk__in=followings).order_by("-timestamp")

    paginator = Paginator(posts, 10)
    page_num = request.GET.get("page", 1)
    try:
        page = paginator.page(page_num)
    except EmptyPage:
        page = paginator.page(1)

    return render(request, "network/feed.html", {
        "posts": page,
        "option": option
    })



# Def related to API

@login_required
def posts(request, option):
    if option.lower() == "all":
        posts = Post.objects.all().order_by("-timestamp")
        return JsonResponse([post.serialize() for post in posts], safe=False)
    if option.lower() == "followings":
        user = request.user
        followings = user.serialize()["followings"]
        posts = Post.objects.filter(user__pk__in=followings).order_by("-timestamp")
        return JsonResponse([post.serialize() for post in posts], safe=False)

@csrf_exempt
@login_required
def post(request, post_id):
    # Query for requested post
    try:
        post = Post.objects.get(user=request.user, pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)

    # Return post content
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update whether email is read or should be archived
    elif request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            post.content = data["content"]
        post.save()
        return HttpResponse(status=204)

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def new_post(request):
    # make a new Post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    content = data.get("content")

    if content == "":
        return JsonResponse({"error": "Post content can not be empty"}, status=400)

    post = Post(user=request.user, content=content)
    post.save()
    return JsonResponse({"message": "Post created successfully"}, status=201)

@csrf_exempt
@login_required
def profile(request, userid):
    # Query for requested User
    try:
        user = User.objects.get(pk=userid)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    # Return post content
    if request.method == "GET":
        return JsonResponse(user.serialize())

    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)

@csrf_exempt
@login_required
def follow(request, userid):
    if request.method == "POST":
        famous = User.objects.get(id=userid)
        follow = Follow(famous=famous, follower=request.user)
        follow.save()
        return HttpResponse(status=204)

@csrf_exempt
@login_required
def unfollow(request, userid):
    if request.method == "POST":
        famous = User.objects.get(id=userid)
        print("famoso " + famous.__str__())
        follow = famous.followers.get(follower=request.user)
        print("follow " + follow.__str__())
        follow.delete()
        return HttpResponse(status=204)
