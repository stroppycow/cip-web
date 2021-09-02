"""URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.views.generic import TemplateView
from django.urls import path,include
from rest_framework.schemas import get_schema_view
from web.views import consulter_index_profession
urlpatterns = [
    path('', consulter_index_profession, name='index-profession'),
    path('openapi', get_schema_view(
            title="API de consultation l'index des professions PCS 2020",
            description="API pour rechercher des entités dans la nomenclature PCS 2020",
            version="1.0.0"
        ), name='openapi-schema'),
    path('api/swagger-ui/', TemplateView.as_view(
        template_name='api/swagger-ui.html',
        extra_context={'schema_url':'openapi-schema'}
    ), name='swagger-ui'),
    path('api', include('api.urls'))
]

