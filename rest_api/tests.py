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

from rest_api.views import ModulePackageViewer,ModuleByNameViewer,package_rate
from rest_api.models import ModulePackage,ModuleHistory,ModuleRank

# Test Data
data = {
        "metadata": {
        	"Name": "smallest",
        	"Version": "1.2.0",
        	"ID": "smallest"
        },
        "data": {
        	"Content": "lajelmvoiejnoawijnm",
        	"JSProgram": "process.exit(1)\n"
            }
    }
update_data = {
        "metadata": {
        	"Name": "smallest",
        	"Version": "2.2.0",
        	"ID": "smallest"
        },
        "data": {
        	"Content": "212154544xdfd",
        	"URL": "https://github.com/bendrucker/smallest",
        	"JSProgram": "\nprocess.exit(1)\n"
            }
    }

# Create your tests here.
    
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
        pkg = ModulePackage.objects.get(ID="smallest")
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
    pkg_endpoint = 'package/byName/'

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

# ============= Package Rate Testing ============ #
    factory = APIRequestFactory()
    pkg_endpoint = 'package/smallest/rate/'
    
    def test_package_rate_unauthorized(self):
        
        # Test Unauthorized Package request
        request = self.factory.get(self.pkg_endpoint)
        response = package_rate(request,pk='TestModule1')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_package_rate_authorized(self):
        
        # Test authorized Package request
        request = self.factory.get(self.pkg_endpoint)
        force_authenticate(request=request,user=self.user)
        response = package_rate(request,pk='smallest')
        #self.assertEqual(response.status_code,status.HTTP_200_OK)
