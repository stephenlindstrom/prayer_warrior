from django.db import models
from django.contrib.auth.models import User

# class Item(models.Model):
#     item_name = models.TextField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.item_name
    
class PrayerRequest(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.content
