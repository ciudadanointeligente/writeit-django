from django.test import TestCase
from writeit.models import WriteItApiInstance
from django.db import IntegrityError

class WriteItApiInstanceTestCase(TestCase):
	def setUp(self):
		pass

	def test_create_instance(self):

		instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
		self.assertTrue(instance)
		self.assertEquals(instance.url, 'http://writeit.ciudadanointeligente.org/api/v1/')


	def test_instances_are_unique(self):
		instance = WriteItApiInstance.objects.create(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
		instance2 = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
		with self.assertRaises(IntegrityError):
			instance2.save()



