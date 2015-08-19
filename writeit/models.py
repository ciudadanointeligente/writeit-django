from django.db import models
from django.conf import settings
from datetime import datetime
from popolo.models import Person
from writeit.apikey_auth import ApiKeyAuth
from django.utils.encoding import force_text
import json
import requests
import time
import re
import slumber
from rest_framework.reverse import reverse
from urlparse import urljoin
from django.contrib.sites.models import Site

class WriteItApiInstance(models.Model):

    url = models.URLField(unique=True)
    def __init__(self, *args, **kwargs):
        super(WriteItApiInstance, self).__init__(*args, **kwargs)
        self.api = slumber.API(self.url, auth=ApiKeyAuth(settings.WRITEIT_USERNAME, settings.WRITEIT_KEY))

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

    def __unicode__(self):
        return "%(name)s at %(api_instance)s"%{
            'name':self.name,
            'api_instance':self.api_instance.url
            }


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

    def push_to_the_api(self, extra_params=None):
        api = self.api_instance.get_api()
        dictified = {'name': self.name}
        if extra_params:
            dictified.update(extra_params)
        response = api.instance._request("POST", data=dictified)
        as_json = json.loads(force_text(response.content))
        self.url = as_json['resource_uri']
        self.remote_id = as_json['id']
        self.save()


class Message(WriteItDocument):
    author_name = models.CharField(max_length=512)
    author_email = models.EmailField()
    subject = models.CharField(max_length=512)
    content = models.TextField()
    writeitinstance = models.ForeignKey(WriteItInstance)
    slug = models.CharField(max_length=512)
    people = models.ManyToManyField(Person, related_name='messages')

    def push_to_the_api(self):
        api = self.api_instance.get_api()
        current_site = Site.objects.get_current()
        persons = []
        for person in self.people.all():
            api_url = urljoin('http://' + current_site.domain, reverse('person-detail', kwargs={'pk': person.id}))
            if api_url.endswith('/'):
                api_url = api_url[:-1]
            persons.append(api_url)

        dictionarized = {
            "author_name": self.author_name,
            "author_email": self.author_email,
            "subject": self.subject,
            "content": self.content,
            "writeitinstance": self.writeitinstance.url,
            "slug": self.slug,
            "persons": persons
            }
        response = api.message._request("POST", data=dictionarized) 
        as_json = json.loads(force_text(response.content))
        self.url = as_json['resource_uri']
        self.remote_id = as_json['id']
        self.save()


class Answer(WriteItDocument):
    content = models.TextField()
    created = models.DateField(null=True)
