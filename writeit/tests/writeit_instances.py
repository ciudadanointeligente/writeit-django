from django.test import TestCase
from writeit.models import WriteItApiInstance

class WriteItApiInstanceTestCase(TestCase):
	def setUp(self):
		pass

	def test_create_instance(self):

		instance = WriteItApiInstance(url= 'http://writeit.ciudadanointeligente.org/api/v1/')
		self.assertTrue(instance)
		self.assertEquals(instance.url, 'http://writeit.ciudadanointeligente.org/api/v1/')



