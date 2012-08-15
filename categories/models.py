from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

class Client(models.Model):
    
    name = models.CharField(max_length=255)
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3)
    
    phone_1 = models.IntegerField(blank=True, null=True)
    phone_2 = models.IntegerField(blank=True, null=True)
    fax = models.IntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

admin.site.register(Client)

class Activity(models.Model):
    code = models.CharField(max_length=5, unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "activities"
        ordering = ['name']

    def __unicode__(self):
        """
        The string representation of an instance of this class
        """
        return self.name

admin.site.register(Activity)

class ProjectManager(models.Manager):
    
    def active(self):
        return self.get_query_set().filter(active=True)

class Project(models.Model):
    
    client = models.ForeignKey(Client)
    name = models.CharField(max_length=10)
    description = models.TextField(blank=True, null=True)
    project_code = models.CharField(max_length=5)
    project_url = models.URLField(blank=True, null=True)
    
    data_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    active = models.BooleanField(default=True)
    
    activities = models.ManyToManyField(Activity, verbose_name=_('activities'), related_name="activities", through='ProjectActivity')
    
    objects = ProjectManager()
    
    def __unicode__(self):
        return self.name
    
admin.site.register(Project)

class ProjectActivity(models.Model):
    class Meta:
        verbose_name_plural = "project_activities"
    
    project = models.ForeignKey(Project, related_name="project", verbose_name=_('project'))
    activity = models.ForeignKey(Activity, related_name="activity")

    def __unicode__(self):
        return 'Project: ' + self.project.name + ", Activity: " + self.activity.name

admin.site.register(ProjectActivity)
