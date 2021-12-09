from django.http import response
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from rest_framework import VERSION
from rest_framework.parsers import JSONParser

from rest_framework.test import APITestCase,APIClient,APIRequestFactory
from rest_framework.test import force_authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_api.views import test_list, ModulePackageViewer,ModuleByNameViewer
from rest_api.models import TestApi,ModulePackage,ModuleHistory

# Test Data
data = {
        "metadata": {
        	"Name": "TestData",
        	"Version": "1.2.0",
        	"ID": "TestData"
        },
        "data": {
        	"Content": "lajelmvoiejnoawijnm",
        	"JSProgram": "process.exit(1)\n"
            }
    }
update_data = {
        "metadata": {
        	"Name": "TestModule1",
        	"Version": "2.2.0",
        	"ID": "TestModule1"
        },
        "data": {
        	"Content": "212154544xdfd",
        	"URL": "https://github.com/test",
        	"JSProgram": "\nprocess.exit(1)\n"
            }
    }

# Create your tests here.
class TestApiTestCase(TestCase):
    factory = APIRequestFactory()
    endpoint = 'api/test/'

    # =========== TestCase Setup =========== #
    def setUp(self):
        # Direct Creation
        TestApi.objects.create(title="TestObject1")
        TestApi.objects.create(title="TestObject2")

        # API setup
        self.user = User.objects.create_user(username='admin',password='admin')

    def test_model_creation(self):
        # This is simply to understand how Django tests are called
        t_obj1 = TestApi.objects.get(title="TestObject1")
        t_obj2 = TestApi.objects.get(title="TestObject2")
        self.assertIsNotNone(t_obj1)
        self.assertIsNotNone(t_obj2)
    
    def test_api_creation(self):
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
    factory = APIRequestFactory()
    pkg_endpoint = 'package/'

    # =========== TestCase Setup =========== #
    def setUp(self):
        # Create a variety of packages
        ModulePackage.objects.create(Name="TestModule1",Version="1.1.1",ID="TestModule1",JSProgram="return")

        self.user = User.objects.create_user(username='admin',password='admin')
    
    def test_setup(self):
        pkg_1 = ModulePackage.objects.get(ID="TestModule1")
        self.assertIsNotNone(pkg_1)

    # ============= POST Testing ============ #
    def test_post_unauthorized(self):

        # Test Unauthorized Package request
        request = self.factory.post(self.pkg_endpoint,data=data,format='json')
        response = (ModulePackageViewer.as_view())(request)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_post_authorized(self):

        # Test Authorized Package request
        request = self.factory.post(self.pkg_endpoint,data=data,format='json')
        force_authenticate(request=request,user=self.user)
        response = (ModulePackageViewer.as_view())(request)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        pkg = ModulePackage.objects.get(ID="TestData")
        self.assertIsNotNone(pkg)

    # ============= GET Testing ============ #
    def test_get_unauthorized(self):

        # Test Unauthorized Package request
        request = self.factory.get(self.pkg_endpoint,kwargs={'pk':'TestModule1'})
        response = (ModulePackageViewer.as_view())(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_get_authorized(self):
        
        # Test Authorized Package request
        request = self.factory.get(self.pkg_endpoint,kwargs={'pk':'TestModule1'})
        force_authenticate(request=request,user=self.user)
        response = (ModulePackageViewer.as_view())(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # ============= PUT Testing ============ #
    def test_put_unauthorized(self):
        
        # Test Unauthorized Package request
        request = self.factory.put(self.pkg_endpoint,data=update_data,kwargs={'pk':'TestModule1'},format='json')
        response = (ModulePackageViewer.as_view())(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_put_authorized(self):

        # Test Authorized Package request
        request = self.factory.put(self.pkg_endpoint,data=update_data,kwargs={'pk':'TestModule1'},format='json')
        force_authenticate(request=request,user=self.user)
        response = (ModulePackageViewer.as_view())(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    # ============= DELETE Testing ============ #
    def test_delete_unauthorized(self):

        # Test Unauthorized Package request
        request = self.factory.delete(self.pkg_endpoint,kwargs={'pk':'TestModule1'})
        response = (ModulePackageViewer.as_view())(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_delete_authorized(self):

        # Test Authorized Package request    
        request = self.factory.delete(self.pkg_endpoint,kwargs={'pk':'TestModule1'})
        force_authenticate(request=request,user=self.user)
        response = (ModulePackageViewer.as_view())(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'message': 'successfully deleted entry.'}
        )
   
 # ============= byName Testing ============ #
    factory = APIRequestFactory()
    pkg_endpoint = 'package/byName'

    def test_byname_unauthorized(self):

        # Test Unauthorized Package request
        request = self.factory.get(self.pkg_endpoint,kwargs={'name':'TestModule1'})
        response = (ModulePackageViewer.as_view())(request,name='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_byname_authorized(self):

        # Test Authorized Package request
        
        request = self.factory.get(self.pkg_endpoint,kwargs={'name':'TestModule1'})
        force_authenticate(request=request,user=self.user)
        response = (ModuleByNameViewer.as_view())(request,name='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
