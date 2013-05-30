from django.test import TestCase
from writeit.models import WriteItApiInstance, WriteItInstance
from django.db import IntegrityError
from unittest import skip
import slumber

class WriteItApiInstanceTestCase(TestCase):
	def setUp(self):
		self.api_instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
		

	def test_create_instance(self):
		self.assertTrue(self.api_instance)
		self.assertEquals(self.api_instance.url, 'http://writeit.ciudadanointeligente.org/api/v1/')


	def test_instances_are_unique(self):
		self.api_instance.save()
		instance2 = WriteItApiInstance(url= self.api_instance.url)
		with self.assertRaises(IntegrityError):
			instance2.save()


	def test_instance_returns_an_slumber_api(self):
		api = self.api_instance.get_api()
		self.assertTrue(isinstance(api, slumber.API) )




from mock import patch
from fixtures import instances

class WriteItInstanceTestCase(TestCase):
	def setUp(self):
		self.api_instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
		self.api_instance.save()


	def test_writeit_instance_creation(self):
		writeitinstance = WriteItInstance.objects.create(api_instance = self.api_instance,
			name='the name of the thing',
			url="/api/v1/instance/1/"
			)

	def test_retrieve_all(self):
		with patch("slumber.Resource.get") as get:
			get.return_value = instances.get_all()
			self.api_instance.get_all()
			post_retrieve_instances = WriteItInstance.objects.all()

			self.assertEquals(post_retrieve_instances.count(), 2)
			self.assertEquals(post_retrieve_instances[0].name, "instance 1")
			self.assertEquals(post_retrieve_instances[1].name, "instance 2")
			self.assertEquals(post_retrieve_instances[0].url, "/api/v1/instance/1/")
			self.assertEquals(post_retrieve_instances[1].url, "/api/v1/instance/2/")
			self.assertEquals(post_retrieve_instances[0].api_instance, self.api_instance)
			self.assertEquals(post_retrieve_instances[1].api_instance, self.api_instance)