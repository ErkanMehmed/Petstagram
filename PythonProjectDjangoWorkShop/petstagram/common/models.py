from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()

class Comment(models.Model):
    text = models.TextField(max_length=300)
    date_time_of_publication = models.DateField(auto_now_add=True,)
    to_photo = models.ForeignKey(to='photos.Photo', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_time_of_publication']

class Like(models.Model):
    to_photo = models.ForeignKey(to='photos.Photo', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
