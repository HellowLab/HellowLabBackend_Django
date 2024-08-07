from django.db import models
from django.conf import settings

#   Movie results track the result of each swipe a user makes
class MovieResult(models.Model):
  id = models.AutoField(primary_key=True)
  user = models.ForeignKey(settings.Auth_USER_MODEL)
  imdbResult = models.CharField(max_length=30)
  swipeResult = models.BooleanField()
  swipeDate = models.DateTimeField(auto_now_add=True)
  watched = models.BooleanField(default=False)
  myRanking = models.IntegerField(null=True, blank=True)
  myComments = models.CharField(max_length=500, null=True, blank=True)

  def __str__(self):
    return self.name