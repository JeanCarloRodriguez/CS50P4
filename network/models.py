from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "userId": self.id,
            "user": self.username,
            "followings": [following.famous.id for following in self.followings.all()],
            "followers": [follower.follower.id for follower in self.followers.all()],
            "posts": [post.serialize() for post in self.posts.all().order_by("-timestamp")]
        }

class Post(models.Model):
    user = models.ForeignKey("User", related_name="posts", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "userId": self.user.id,
            "user": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "likes": self.likes
        }
    def __str__(self):
        return f'{self.user} {self.content}'

class Follow(models.Model):
    famous = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    follower = models.ForeignKey(User, related_name="followings", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["famous", "follower"]

    def __str__(self):
        return f"{self.follower.username} is following {self.famous.username}"