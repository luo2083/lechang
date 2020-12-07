from django.db import models


class App(models.Model):
    appid = models.CharField(primary_key=True, max_length=32)
    category = models.CharField(max_length=128)
    application = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    published_date = models.DateField()
    url = models.CharField(max_length=128)
    desc = models.TextField()


    def to_dict(self):
        return {
            'appid': self.appid,
            'category': self.category,
            'application': self.application,
            'name': self.name,
            'published_date': self.published_date,
            'url': self.url,
            'desc': self.desc
        }
    def __str__(self):
        return '%s(%s)' %(self.name, self.application)

    def __repr__(self):
        return str(self.to_dict())