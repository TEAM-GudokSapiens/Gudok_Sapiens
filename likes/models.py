from django.db import models

class Dib(models.Model):
    service = models.ForeignKey(
        "services.Service", on_delete=models.CASCADE, db_column="service_id")
    users = models.ForeignKey("users.User", related_name='users_dibs', on_delete=models.CASCADE, db_column="user_id")
    created_at = models.DateTimeField(auto_now_add=True)


