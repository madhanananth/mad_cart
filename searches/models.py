from django.db import models
from django.conf import settings

# Create your models here.

class SearchHistory(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True )
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        if self.user :
            return f"{self.user.usename} searched '{self.query}'"
        
        return f"Anonymous searched '{self.query}'"
