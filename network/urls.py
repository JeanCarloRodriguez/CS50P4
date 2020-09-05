
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("feed/<str:option>", views.feed, name="feed"),
    path("followings", views.followings_view, name="followings"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.profile_view, name="profile_view"),

    # API Routes
    path("post/<int:post_id>", views.post, name="post"),
    path("posts/<str:option>", views.posts, name="posts"),
    # path("allPosts/", views.all_posts, name="all_posts"),
    path("user/profile/<int:userid>", views.profile, name="profile"),
    path("user/post/new_post", views.new_post, name="new_post"),
    path("user/follow/<str:userid>", views.follow, name="follow"),
    path("user/unfollow/<str:userid>", views.unfollow, name="unfollow")
]
