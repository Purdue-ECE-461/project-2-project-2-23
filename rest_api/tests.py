from django.test import TestCase
from rest_framework import VERSION
from rest_framework.parsers import JSONParser
from rest_api.models import TestApi,ModulePackage

# Create your tests here.
class TestApiTestCase(TestCase):
    def setUp(self):
        TestApi.objects.create(title="TestObject1")
        TestApi.objects.create(title="TestObject2")
    
    def test_creation(self):
        # This is simply to understand how Django tests are called
        t_obj1 = TestApi.objects.get(title="TestObject1")
        t_obj2 = TestApi.objects.get(title="TestObject2")
        self.assertIsNotNone(t_obj1)
        self.assertIsNotNone(t_obj2)

class ModulePackageTestCase(TestCase):
    def setUp(self):
        # Create a variety of packages
        ModulePackage.objects.create(Name="TestModule1",Version="1.1.1",ID="TestModule1",JSProgram="return")
    
    def test_creation(self):
        pkg_1 = ModulePackage.objects.get(ID="TestModule1")
        self.assertIsNotNone(pkg_1)