# coding=utf-8
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
from popit.tests import instance_helpers
import os
import subprocess


def popit_load_data(fixture_name='default'):

    """
    Use the mongofixtures CLI tool provided by the pow-mongodb-fixtures package
    used by popit-api to load some test data into db. Don't use the test fixture
    from popit-api though as we don't want changes to that to break our test
    suite.

        https://github.com/powmedia/pow-mongodb-fixtures#cli-usage

    """
    instance_helpers.delete_api_database()
    project_root = os.path.normpath(os.path.join(os.path.dirname(__file__),'../..'))
    
    # gather the args for the call
    mongofixtures_path = os.path.join( project_root, 'popit-api-for-testing/node_modules/.bin/mongofixtures' )
    database_name      = instance_helpers.get_api_database_name()
    test_fixtures_path = os.path.join( project_root, 'writeit/tests/fixtures/%s.js'%fixture_name )

    # Check that the fixture exists
    if not os.path.exists(test_fixtures_path):
        raise Exception("Could not find fixture for %s at %s" % (fixture_name, test_fixtures_path))

    # Hack to deal with bad handling of absolute paths in mongofixtures.
    # Fix: https://github.com/powmedia/pow-mongodb-fixtures/pull/14
    test_fixtures_path = os.path.relpath( test_fixtures_path )

    # Usage: mongofixtures db_name path/to/fixtures.js
    dev_null = open(os.devnull, 'w')
    exit_code = subprocess.call([mongofixtures_path, database_name, test_fixtures_path], stdout=dev_null)
    if exit_code:
        raise Exception("Error loading fixtures for '%s'" % fixture_name)   


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


import urllib
from mock import patch, MagicMock
from fixtures import instances
import simplejson as json

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


    def test_unicode(self):
        writeitinstance = WriteItInstance.objects.create(api_instance = self.api_instance,
            name='the name of the thing',
            url="/api/v1/instance/1/",
            remote_id=1
            )
        self.assertEquals(writeitinstance.__unicode__(), 'the name of the thing at http://writeit.ciudadanointeligente.org/api/v1/')


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

    def test_I_can_post_a_writeit_instance(self):
        api_instance = WriteItApiInstance.objects.create(url= settings.LOCAL_TESTING_WRITEIT)
        writeitinstance = WriteItInstance.objects.create(api_instance = api_instance, name='the name of the thing')
        writeitinstance.push_to_the_api()
        self.assertTrue(writeitinstance.url)
        self.assertTrue(writeitinstance.remote_id)


        api = api_instance.get_api()
        response = api.instance(writeitinstance.remote_id).get()
        # writeit returns this when 
        # getting http://localhost:2425/api/v1/instance/2/?format=json&username=admin&api_key=a
        # {
        # id: 2,
        # messages_uri: "/api/v1/instance/2/messages/",
        # moderation_needed_in_all_messages: false,
        # name: "instance 2",
        # rate_limiter: 0,
        # resource_uri: "/api/v1/instance/2/",
        # slug: "instance2"
        # }
        self.assertEquals(response['name'], writeitinstance.name)

    def test_I_can_post_a_writeit_instance_with_a_popit_api(self):

        popit_load_data()


        api_instance = WriteItApiInstance.objects.create(url= settings.LOCAL_TESTING_WRITEIT)
        writeitinstance = WriteItInstance.objects.create(api_instance = api_instance, name='the name of the thing')
        writeitinstance.push_to_the_api(extra_params={
            'popit-api': settings.TEST_POPIT_API_URL
            })
        self.assertTrue(writeitinstance.url)
        self.assertTrue(writeitinstance.remote_id)
        api = api_instance.get_api()
        response = api.instance(writeitinstance.remote_id).get()
        self.assertEquals(response['name'], writeitinstance.name)
        self.assertEquals(len(response['persons']), 2)
        

        popit_instance = PopitApiInstance.objects.create(url= settings.TEST_POPIT_API_URL)
        popit_instance.fetch_all_from_api()
        persons = Person.objects.filter(api_instance=popit_instance)
        fiera = Person.objects.get(name="Fiera Feroz")
        raton = Person.objects.get(name="Ratón Inteligente")
        #Checking that Fiera and Ratón are in the persons array
        self.assertIn(raton.popit_url, response['persons'])
        self.assertIn(fiera.popit_url, response['persons'])



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
                "persons":['http://popit.org/api/v1/persons/3']
                })
    @skip("I must first fix problem in travis CI")
    def test_when_posting_to_the_api_writeit_message_gets_a_remote_uri(self):
        message = Message.objects.create(api_instance=self.api_instance
            , author_name='author'
            , author_email='author email'
            , subject = 'subject'
            , content = 'content'
            , writeitinstance = self.writeitinstance
            , slug = 'subject-slugified'
            )



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




