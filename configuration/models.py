from django.db import models
from django.contrib.auth.models import User
from categories.models import Project
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class UserProfile(models.Model):
    '''
        user profile
    '''
    class Meta:
        db_table = 'user_profile'        

    user = models.ForeignKey(User, unique=True)
    projects = models.ManyToManyField(Project, verbose_name=_('user_projects'), related_name="user_projects", through='UserProject')

class UserProject(models.Model):
    user_profile = models.ForeignKey(UserProfile)
    project = models.ForeignKey(Project)
    last_updated = models.DateTimeField(auto_now=True)    
    
    class Meta:        
        unique_together = (("user_profile", "project"),)
