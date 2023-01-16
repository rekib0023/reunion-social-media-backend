from django.db import models


class Posts(models.Model):
    title = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=250, null=False)
    created_by = models.ForeignKey("user.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.title


class PostLike(models.Model):
    post = models.ForeignKey(
        "Posts", related_name="likes_set", on_delete=models.CASCADE
    )
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class PostComment(models.Model):
    post = models.ForeignKey(
        "Posts", related_name="comments_set", on_delete=models.CASCADE
    )
    comment = models.CharField(max_length=100, null=False)
    commented_by = models.ForeignKey("user.User", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
