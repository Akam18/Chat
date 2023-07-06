from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", verbose_name="Sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reseiver", verbose_name="Reseiver")
    message = models.CharField(max_length=500, verbose_name="Message")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    is_read = models.BooleanField(default=True, verbose_name="IS READ")

    def str(self) -> str:
        return f"{self.date} {self.sender} -> {self.receiver}: {self.message}"
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-date"]