from django.db import models
from django.conf import settings

#   Movie results track the result of each swipe a user makes
class MovieResult(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  tmdb_id = models.CharField(max_length=30)
  name = models.CharField(max_length=100)
  poster = models.CharField(max_length=100, null=True)
  liked = models.BooleanField()
  swipeDate = models.DateTimeField(auto_now_add=True)
  watched = models.BooleanField(default=False)
  myRanking = models.IntegerField(null=True, blank=True)
  myComments = models.CharField(max_length=500, null=True, blank=True)

  def __str__(self):
    return (f"{self.tmdb_id}")