from django.db import models


class Headlines(models.Model):
    title = models.CharField(max_length=300)
    link = models.CharField(max_length=300)
    time_added = models.DateTimeField('time added')

    def __str__(self):
        return "Title: {}, link: {}, time added: {}".format(self.title, self.link, self.time_added)
