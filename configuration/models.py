from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from categories.models import Project, Taxonomy

class UserProfile(models.Model):
    '''
        user profile
    '''
    user = models.ForeignKey(User)
    taxonomy = models.ForeignKey(Taxonomy)
    projects = models.ManyToManyField(Project, verbose_name=_('user_projects'), related_name="user_projects", through='UserProject')
    configured = models.BooleanField(verbose_name=_('configured'), default=False)
    
    class Meta:
        unique_together = (("user", "taxonomy"),)

class UserProject(models.Model):
    """Stores projects for each user"""
    
    user_profile = models.ForeignKey(UserProfile)
    project = models.ForeignKey(Project)
    last_updated = models.DateTimeField(auto_now=True)    
    
    class Meta:        
        unique_together = (("user_profile", "project"),)
