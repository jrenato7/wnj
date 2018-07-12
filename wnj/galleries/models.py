from django.db import models


from wnj.accounts.models import User


class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField()
    created_at = models.DateField(auto_now=True)
    approved = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'galleries'
        ordering = ('-created_at', )

    def __str__(self):
        return self.user
