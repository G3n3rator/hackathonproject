from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    '''
    AbstractUserを継承する。構文エラーとならないようにpassする
    '''
    pass
