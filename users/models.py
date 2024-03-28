from django.db import models

# Create your models here.

class Code(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='code')
    code = models.CharField(max_length=6)
    expiry_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.code}'