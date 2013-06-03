from django.db import models
from django.conf import settings
from datetime import datetime
import time
import slumber

class WriteItApiInstance(models.Model):

    url = models.URLField(unique=True)
    def __init__(self, *args, **kwargs):
        super(WriteItApiInstance, self).__init__(*args, **kwargs)
        self.api = slumber.API(self.url)

    def get_api(self):
        api = self.api
        return api

    def get_all(self):
        models = [WriteItInstance]

        for model in models:
            model.get_all(api_instance=self)


class WriteItDocument(models.Model):
    api_instance = models.ForeignKey(WriteItApiInstance)
    url = models.CharField(max_length=256)
    remote_id = models.IntegerField(null=True)


class WriteItInstance(WriteItDocument):
    name = models.CharField(max_length=255)
    @classmethod
    def get_all(cls, api_instance):
        api = api_instance.get_api()
        objects = api.instance.get(username=settings.WRITEIT_USERNAME, api_key=settings.WRITEIT_KEY)['objects']
        for api_object in objects:
            instance = cls.objects.create(
                    remote_id=api_object['id'],
                    api_instance=api_instance,
                     url=api_object['resource_uri'],
                     name=api_object['name'])


    def fetch_messages(self, remote_id):
        api = self.api_instance.get_api()
        objects = api.instance(remote_id).messages.get(username=settings.WRITEIT_USERNAME, api_key=settings.WRITEIT_KEY)["objects"]
        for message_dict in objects:
            message = Message.objects.create(
                remote_id=message_dict['id'],
                writeitinstance=self,
                api_instance=self.api_instance,
                author_email= message_dict["author_email"],
                author_name= message_dict["author_name"],
                content= message_dict["content"],
                subject= message_dict["subject"],
                url= message_dict['resource_uri']
                )
            for answer_dict in message_dict['answers']:
                answer = Answer.objects.create(
                    api_instance=self.api_instance,
                    content = answer_dict["content"],
                    remote_id = answer_dict["id"]
                    )




class Message(WriteItDocument):
    author_name = models.CharField(max_length=512)
    author_email = models.EmailField()
    subject = models.CharField(max_length=512)
    content = models.TextField()
    writeitinstance = models.ForeignKey(WriteItInstance)
    slug = models.CharField(max_length=512)

class Answer(WriteItDocument):
    content = models.TextField()
    created = models.DateField(null=True)