from django.conf.urls import url
from django.urls.resolvers import URLPattern
from rest_api import views

urlpatterns = [
    url(r'^api/test', views.test_list),
    url(r'^packages',views.package_list),
    url(r'^package',views.package_detail)
]