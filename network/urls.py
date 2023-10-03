
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newPost", views.newPost, name="newPost"),
    path("profile_page/<int:user_id>", views.profile_page, name="profile_page"),
    path("unfollow", views.unfollow, name="unfollow"),
    path("follow", views.follow, name="follow"),
    path("follows", views.follows, name="follows"),
    path("follows", views.follows, name="follows"),
    path("editPost/<int:post_id>", views.editPost, name="editPost"),
    path("unlike/<int:post_id>", views.unlike, name="unlike"),
    path("give_like/<int:post_id>", views.give_like, name="give_like"),
]
