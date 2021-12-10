from django.conf.urls import url
from django.urls import path
from django.urls.resolvers import URLPattern
from rest_api import views

urlpatterns = [
    path('package',views.ModulePackageViewer.as_view(),name='ModulePackageViewer'),
    path(r'package/<str:pk>/rate',views.package_rate),
    path('package/byName/<str:name>',views.ModuleByNameViewer.as_view(),name='ModuleByNameViewer'),
    path('package/<str:pk>',views.ModulePackageViewer.as_view(),name='ModulePackageViewer'),
    path('packages',views.ModuleListViewer.as_view({'get': 'list'}),name='ModuleListViewer'),
    url(r'reset',views.reset_registry)
]