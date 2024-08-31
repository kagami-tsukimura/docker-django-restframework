# Django 環境作成手順

## Docker 環境構築

```bash
cd backend/ && docker-compose run backend django-admin startproject backend . && docker-compose up -d
```

## Django バージョン確認方法

バージョン確認。

```bash
pip index versions django
pip index versions djangorestframework
pip index versions django-cors-headers
pip index versions psycopg2
```

install する。

```bash
pip install django==4.2.15
pip install djangorestframework==3.15.2
pip install django-cors-headers==4.4.0
pip install psycopg2==2.9.9
```

## swagger 追加方法

下記の修正を行う。

```bash
pip install drf-yasg
```

```txt: requirements.txt
drf-yasg==1.21.7
```

```python: settings.py
INSTALLED_APPS = [
    # 追加項目: swagger
    "rest_framework",
    "drf_yasg",
]


# 追加項目: swagger
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}
```

```python: urls.py
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version="v1",
        description="API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
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
```

サーバーを再起動し、`/swagger/`で Swagger UI が、`/redoc/`で Redoc が表示される。

Swagger UI: http://localhost:8000/swagger/
Redoc: http://localhost:8000/redoc/
