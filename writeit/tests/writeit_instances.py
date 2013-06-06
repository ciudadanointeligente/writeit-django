from django.test import TestCase
from writeit.models import WriteItApiInstance, WriteItInstance, Message, Answer
from django.db import IntegrityError
from unittest import skip
import slumber
from django.conf import settings
from datetime import datetime
from unittest import skip
from popit.models import ApiInstance as PopitApiInstance, Person
from writeit.apikey_auth import ApiKeyAuth

class WriteItApiInstanceTestCase(TestCase):
    def setUp(self):
        self.api_instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org')
        

    def test_create_instance(self):
        self.assertTrue(self.api_instance)
        self.assertEquals(self.api_instance.url, 'http://writeit.ciudadanointeligente.org')


    def test_instances_are_unique(self):
        self.api_instance.save()
        instance2 = WriteItApiInstance(url= self.api_instance.url)
        with self.assertRaises(IntegrityError):
            instance2.save()


    def test_instance_returns_an_slumber_api(self):
        api = self.api_instance.get_api()
        self.assertTrue(isinstance(api, slumber.API) )

    def test_instance_api_with_auth(self):
        api = self.api_instance.get_api()
        auth = api._store['session'].auth
        self.assertTrue(isinstance(auth, ApiKeyAuth))
        self.assertEquals(auth.username, settings.WRITEIT_USERNAME)
        self.assertEquals(auth.api_key, settings.WRITEIT_KEY)



from mock import patch, MagicMock
from fixtures import instances

class WriteItInstanceTestCase(TestCase):
    def setUp(self):
        self.api_instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
        self.api_instance.save()



    def test_writeit_instance_creation(self):
        writeitinstance = WriteItInstance.objects.create(api_instance = self.api_instance,
            name='the name of the thing',
            url="/api/v1/instance/1/",
            remote_id=1
            )
        self.assertTrue(writeitinstance)
        self.assertEquals(writeitinstance.api_instance, self.api_instance)
        self.assertEquals(writeitinstance.name, 'the name of the thing')
        self.assertEquals(writeitinstance.url, "/api/v1/instance/1/")
        self.assertEquals(writeitinstance.remote_id, 1)


    def test_retrieve_all2(self):
        from slumber import Resource
        with patch("slumber.Resource", spec=True) as Resource:
            #Faking the response
            api = Resource.return_value
            api.instance = Resource.return_value
            api.instance.get.return_value = instances.get_all()
            #Making the call to the api
            self.api_instance.get_all()

            #Now Assertions come
            api.instance.get.assert_called_with(username=settings.WRITEIT_USERNAME, api_key=settings.WRITEIT_KEY)

            post_retrieve_instances = WriteItInstance.objects.all()
            self.assertEquals(post_retrieve_instances.count(), 2)
            self.assertEquals(post_retrieve_instances[0].remote_id, 1)
            self.assertEquals(post_retrieve_instances[1].remote_id, 2)
            self.assertEquals(post_retrieve_instances[0].name, "instance 1")
            
            self.assertEquals(post_retrieve_instances[1].name, "instance 2")

            self.assertEquals(post_retrieve_instances[0].url, "/api/v1/instance/1/")
            self.assertEquals(post_retrieve_instances[1].url, "/api/v1/instance/2/")
            self.assertEquals(post_retrieve_instances[0].api_instance, self.api_instance)
            self.assertEquals(post_retrieve_instances[1].api_instance, self.api_instance)




class MessageTestCase(TestCase):
    def setUp(self):
        self.api_instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org')
        self.api_instance.save()
        self.writeitinstance = WriteItInstance.objects.create(api_instance = self.api_instance,
            name='the name of the thing',
            url="/api/v1/instance/1/"
            )
        self.popit_api_instance = PopitApiInstance.objects.create(url='http://popit.org/api/v1')
        self.person1 = Person.objects.create(
            api_instance=self.popit_api_instance, 
            name= "Felipe", 
            popit_url= 'http://popit.org/api/v1/persons/3')


    def test_message_instanciate(self):
        message = Message.objects.create(api_instance=self.api_instance
            , author_name='author'
            , author_email='author email'
            , subject = 'subject'
            , content = 'content'
            , writeitinstance = self.writeitinstance
            , slug = 'subject-slugified'
            )
        message.people.add(self.person1)

        self.assertTrue(message)
        self.assertEquals(message.api_instance, self.api_instance)
        self.assertEquals(message.author_name, 'author')
        self.assertEquals(message.author_email, 'author email')
        self.assertEquals(message.subject, 'subject')
        self.assertEquals(message.content, 'content')
        self.assertEquals(message.writeitinstance, self.writeitinstance)
        self.assertEquals(message.slug, 'subject-slugified')
        self.assertEquals(message.people.all().count(), 1)
        self.assertEquals(message.people.all()[0], self.person1)





class MessageRemoteGetterTestCase(TestCase):
    def setUp(self):
        self.api_instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
        self.api_instance.save()
        self.writeitinstance = WriteItInstance.objects.create(api_instance = self.api_instance,
            name='the name of the thing',
            url="/api/v1/instance/1/"
            )

        self.popit_api_instance = PopitApiInstance.objects.create(url='http://popit.org/api/v1')
        self.person1 = Person.objects.create(
            api_instance=self.popit_api_instance, 
            name= "Felipe", 
            popit_url= 'http://popit.org/api/v1/persons/3')


    #@skip("create messages with people")
    def test_message_post_to_the_API(self):
        with patch("slumber.Resource", spec=True) as Resource:
            api = Resource.return_value
            api.message = Resource.return_value
            message = Message.objects.create(api_instance=self.api_instance
            , author_name='author'
            , author_email='author email'
            , subject = 'subject'
            , content = 'content'
            , writeitinstance = self.writeitinstance
            , slug = 'subject-slugified'
            )
            message.people.add(self.person1)


            message.push_to_the_api()

            api.message.post.assert_called_with({
                "author_name":'author',
                "author_email":'author email',
                "subject" : 'subject',
                "content" : 'content',
                "writeitinstance" : self.writeitinstance.url,
                "slug" : 'subject-slugified',
                "people":['http://popit.org/api/v1/persons/3']
                })

    def test_when_I_fetch_an_instance_it_brings_all_its_messages_as_well(self):
        with patch("slumber.Resource", spec=True) as Resource:
            api = Resource.return_value
            api.instance = Resource.return_value
            api.instance.return_value = Resource.return_value
            api.instance.return_value.messages = Resource.return_value
            api.instance.return_value.messages.get.return_value = instances.get_messages_for_instance1()

            self.writeitinstance.fetch_messages(1)
            api.instance.assert_called_with(1)

            api.instance(1).messages.get.assert_called_with(
                username=settings.WRITEIT_USERNAME, 
                api_key=settings.WRITEIT_KEY)


            created_messages = Message.objects.all()

            self.assertEquals(created_messages.count(), 2)
            self.assertEquals(created_messages[0].author_email, "luisfelipealvarez@gmail.com")
            self.assertEquals(created_messages[0].remote_id, 1)
            self.assertEquals(created_messages[0].author_name, "Felipi poo")
            self.assertEquals(created_messages[0].content, "Quiero probar esto")
            self.assertEquals(created_messages[0].url, "/api/v1/message/1/")
            self.assertEquals(created_messages[0].subject, "Probando probando")

    def test_get_all_messages_with_answers(self):
        with patch("slumber.Resource", spec=True) as Resource:
            api = Resource.return_value
            api.instance = Resource.return_value
            api.instance.return_value = Resource.return_value
            api.instance.return_value.messages = Resource.return_value
            api.instance.return_value.messages.get.return_value = instances.get_messages_for_instance1()
            self.writeitinstance.fetch_messages(1)

            answers = Answer.objects.all()
            self.assertTrue(answers.count(), 1)
            self.assertEquals(answers[0].content, "weeena")
            self.assertEquals(answers[0].remote_id, 1)




