"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from sample.views import (  # AreaMasterRetrieveUpdateDestroyAPIView,
    AreaMasterListCreateAPIView,
    ExampleModelListCreateAPIView,
    ExampleModelRetrieveUpdateDestroyAPIView,
)

from .views import HelloWorldAPIView, JSONPlaceholderAPIView

schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


def custom_home(request):
    return HttpResponse("Welcome to the Custom Home Page!")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", custom_home, name="home"),
    path("hello/", HelloWorldAPIView.as_view(), name="hello-world"),
    path("json/", JSONPlaceholderAPIView.as_view(), name="json-placeholder"),
    # ExampleModelのCRUDエンドポイント
    path(
        "examplemodel/",
        ExampleModelListCreateAPIView.as_view(),
        name="examplemodel-list-create",
    ),
    path(
        "examplemodel/<int:pk>/",
        ExampleModelRetrieveUpdateDestroyAPIView.as_view(),
        name="examplemodel-detail",
    ),
    # AreaMasterのCRUDエンドポイント
    path(
        "areamaster/",
        AreaMasterListCreateAPIView.as_view(),
        name="areamaster-list-create",
    ),
    # path(
    #     "areamaster/<int:pk>/",
    #     AreaMasterRetrieveUpdateDestroyAPIView.as_view(),
    #     name="areamaster-detail",
    # ),
    # Swagger UI
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # Redoc
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
