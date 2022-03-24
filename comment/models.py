from django.db import models

from django.db import models


class Created(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Comment(Created):
    comment = models.TextField()
    author = models.ForeignKey(
        "account.User",
        related_name="comments",
        on_delete=models.DO_NOTHING
    )
    post = models.ForeignKey(
        "post.Post",
        related_name="comments",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.author} -> {self.comment}"

    class Meta:
        ordering = ("-created", )
