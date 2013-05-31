from django.db import models
from django.conf import settings
import slumber

class WriteItApiInstance(models.Model):

    url = models.URLField(unique=True)

    def get_api(self):
        api = slumber.API(self.url)
        return api

    def get_all(self):
        models = [WriteItInstance]

        for model in models:
            model.get_all(api_instance=self)


class WriteItDocument(models.Model):
    api_instance = models.ForeignKey(WriteItApiInstance)
    url = models.CharField(max_length=256)


class WriteItInstance(WriteItDocument):
    name = models.CharField(max_length=255)
    @classmethod
    def get_all(cls, api_instance):
        api = api_instance.get_api()
        objects = api.instance.get(username=settings.WRITEIT_USERNAME, api_key=settings.WRITEIT_KEY)['objects']
        for api_object in objects:
            instance = cls.objects.create(api_instance=api_instance,
                     url=api_object['resource_uri'],
                     name=api_object['name'])


    def fetch_messages(self):
        api = self.api_instance.get_api()
        objects = api.instance.messages.get(username=settings.WRITEIT_USERNAME, api_key=settings.WRITEIT_KEY)



class Message(WriteItDocument):
    author_name = models.CharField(max_length=512)
    author_email = models.EmailField()
    subject = models.CharField(max_length=512)
    content = models.TextField()
    writeitinstance = models.ForeignKey(WriteItInstance)
    slug = models.CharField(max_length=512)