from django.http import response
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework import VERSION
from rest_framework.parsers import JSONParser

from rest_framework.test import APITestCase,APIClient,APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_api.views import test_list
from rest_api.models import TestApi,ModulePackage

# Create your tests here.
class TestApiTestCase(TestCase):
    factory = APIRequestFactory()
    endpoint = 'api/test/'

    def setUp(self):
        # Direct Creation
        TestApi.objects.create(title="TestObject1")
        TestApi.objects.create(title="TestObject2")

        # API setup
        self.user = User.objects.create_user(username='admin',password='admin')
        '''self.user = User.objects.create_user(username='admin',password='admin')
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_X_AUTHORIZATION='bearer '+self.token.key)'''


    def test_model_creation(self):
        # This is simply to understand how Django tests are called
        t_obj1 = TestApi.objects.get(title="TestObject1")
        t_obj2 = TestApi.objects.get(title="TestObject2")
        self.assertIsNotNone(t_obj1)
        self.assertIsNotNone(t_obj2)
    
    def test_api_creation(self):
        '''TEST API RESPONSES'''
        # Case 1: No authorization provided
        request = self.factory.post(self.endpoint, data={'title':'testData'})
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # Case 2: Post to database and retreive
        request = self.factory.post(self.endpoint,{'title':'testTitle'},format='json')
        force_authenticate(request=request,user=self.user)
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_api_retreival(self):
        # Case 1: request without authorization
        request = self.factory.get(self.endpoint)
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # Case 2: Make a post request and check if test database is valid
        request = self.factory.post(self.endpoint,{'title':'testTitle'},format='json')
        force_authenticate(request=request,user=self.user)
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        request = self.factory.get(self.endpoint)
        force_authenticate(request=request,user=self.user)
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            [{'id': 1, 'title': 'TestObject1'}, {'id': 2, 'title': 'TestObject2'}, {'id': 3, 'title': 'testTitle'}]
        )
    
    def test_api_deletion(self):
        # Case 1: request without authorization
        request = self.factory.delete(self.endpoint)
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

        # Case 2: delete all testAPI
        request = self.factory.delete(self.endpoint)
        force_authenticate(request=request,user=self.user)
        response = test_list(request)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

class ModulePackageTestCase(TestCase):
    def setUp(self):
        # Create a variety of packages
        ModulePackage.objects.create(Name="TestModule1",Version="1.1.1",ID="TestModule1",JSProgram="return")
    
    def test_creation(self):
        pkg_1 = ModulePackage.objects.get(ID="TestModule1")
        self.assertIsNotNone(pkg_1)