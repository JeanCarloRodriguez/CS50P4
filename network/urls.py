
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("followings", views.followings_view, name="followings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:username>", views.profile_view, name="profile_view"),

    # API Routes
    path("post/<int:postid>", views.post, name="post"),
    path("posts/<str:option>", views.posts, name="posts"),
    # path("allPosts/", views.all_posts, name="all_posts"),
    path("profile/<int:userid>", views.profile, name="profile"),
    path("post/new_post", views.new_post, name="new_post"),
    path("follow/<str:userid>", views.follow, name="follow"),
    path("unfollow/<str:userid>", views.unfollow, name="unfollow")
]
