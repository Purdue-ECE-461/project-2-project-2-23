from django.conf.urls import url
from django.urls import path
from django.urls.resolvers import URLPattern
from rest_api import views

urlpatterns = [
    url(r'^api/test/', views.test_list),
    url(r'^packages/',views.package_list),
    url(r'^package/byName/<str:pk>/',views.package_by_name),
    path('package/',views.ModulePackageViewer.as_view(),name='ModulePackageViewer'),
    path('package/<str:pk>/',views.ModulePackageViewer.as_view(),name='ModulePackageViewer'),
    url(r'reset/',views.reset_registry)
]
