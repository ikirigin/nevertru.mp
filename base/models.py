from django.db import models
from django.contrib.auth.models import User
import base64

class Pledge(models.Model):
    user = models.ForeignKey(User, db_index=True)
    party = models.CharField(max_length=40, db_index=True)
    code = models.CharField(max_length=40, db_index=True)
    created_at = models.DateTimeField(null=True, db_index=True, auto_now_add=True)
    verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, db_index=True)
    verified_by = models.ForeignKey(User, db_index=True, related_name='verifier')
    
    @classmethod
    def user_create(user, party):
        try:
            pledge = Pledge.objects.filter(user=user)[0]
            return pledge
        except:
            pass
        pledge = Pledge(user=user, party=party)
        pledge.save()
        code = base64.b64encode(str(pledge.pk))
        pledge.save()
        return pledge

