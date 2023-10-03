from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    contenido = models.CharField(max_length=140)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="autor")
    date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post {self.id} made by {self.usuario} on {self.date.strftime('%d %b %Y %H:%M:%S')}"
    
class Following(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_followed")

    def __str__(self):
        return f"{self.user} is folowing {self.followed}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="like_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")

    def __str__(self):
        return f"{self.user} liked {self.post}"
