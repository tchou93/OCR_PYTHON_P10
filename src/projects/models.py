from django.db import models
from django.conf import settings

CHOICES_TYPE = [
    ('BACK-END', 'BACK-END'),
    ('FRONT-END', 'FRONT-END'),
    ('IOS', 'IOS'),
    ('ANDROID', 'ANDROID')
]
CHOICES_PRIORITY = [
    ('LOW', 'LOW'),
    ('MEDIUM', 'MEDIUM'),
    ('HIGH', 'HIGH')
]

CHOICES_TAG = [
    ('BUG', 'BUG'),
    ('IMPROVEMENT', 'IMPROVEMENT'),
    ('TASK', 'TASK')
]

CHOICES_STATUS = [
    ('TO-DO', 'TO-DO'),
    ('IN-PROGRESS', 'IN-PROGRESS'),
    ('DONE', 'DONE')
]

CHOICES_PERMISSION = [
    ('CONTRIBUTOR', 'CONTRIBUTOR'),
    ('AUTHOR', 'AUTHOR'),
]


class Project(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=50, choices=CHOICES_TYPE)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Project({self.title})"

class Contributor(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=CHOICES_PERMISSION)
    def __str__(self):

        return f"Contributor({self.user})"

class Issue(models.Model):
    title = models.CharField(max_length=128)
    desc = models.TextField(blank=True)
    tag = models.CharField(max_length=50, choices=CHOICES_TAG)
    priority = models.CharField(max_length=50, choices=CHOICES_PRIORITY)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=CHOICES_STATUS)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assignee = models.ForeignKey(to=Contributor, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Issue({self.title})"

class Comment(models.Model):
    description = models.TextField(blank=True)
    author = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Comment({self.author.name} => {self.issue.title})"