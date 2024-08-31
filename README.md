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

## postgresql 接続方法

- ※ 同一アプリケーション内で複数テーブル作る場合は、3. から行う。

1. コンテナ内に入りアプリケーション作成（ここでは `sample`）。

   ```bash
   docker exec -it <コンテナ名> bash

   # `sample`は任意のDjangoアプリ名
   python3 manage.py startapp sample
   ```

2. 設定ファイルに作成したアプリケーションを追加する。

   ```python: settings.py
   INSTALLED_APPS = [
       # 追加項目: postgresql
       "sample", # <任意のDjangoアプリ名>
   ]
   ```

3. テーブルを作成する。

   ```python: sample/models.py
   from django.db import models

   class ExampleModel(models.Model):
       name = models.CharField(max_length=100)
       description = models.TextField()

       def __str__(self):
           return self.name
   ```

4. コンテナ内に入りマイグレーションファイル作成。

   ```bash
   docker exec -it <コンテナ名> bash # コンテナ内なら不要

   python manage.py makemigrations sample # sample: <任意のDjangoアプリ名>
   ```

5. コンテナ内でマイグレーション実行。

   ```bash
   docker exec -it <コンテナ名> bash # コンテナ内なら不要

   python manage.py migrate
   ```

6. テーブル確認(pgadmin 等)。  
   DB に接続して、`sample_<models.py のクラス名>`テーブルの存在を確認。

## CRUD(DB)

1. シリアライザーの作成（ここでは `sample`）。

   ```bash
   touch sample/serializers.py
   ```

   ```python: sample/serializers.py
   from rest_framework import serializers
   from .models import ExampleModel


   class ExampleModelSerializer(serializers.ModelSerializer):
       class Meta:
           model = ExampleModel
           # モデルの全フィールドをシリアライズ
           fields = "__all__"
   ```

2. CRUD 処理用のビューを作成（ここでは `sample`）。

   ```python: sample/views.py
   from rest_framework import generics

   from .models import ExampleModel
   from .serializers import ExampleModelSerializer


   class ExampleModelListCreateAPIView(generics.ListCreateAPIView):
       queryset = ExampleModel.objects.all()
       serializer_class = ExampleModelSerializer


   class ExampleModelRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
       queryset = ExampleModel.objects.all()
       serializer_class = ExampleModelSerializer
   ```

3. ビューを URL パターンに追加。

   ```python: backend/urls.py
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
   from sample.views import (
       ExampleModelListCreateAPIView,
       ExampleModelRetrieveUpdateDestroyAPIView,
   )

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
       path("admin/", admin.site.urls),
       # ExampleModelのCRUDエンドポイント
       # GET, POST
       path(
           "examplemodel/",
           ExampleModelListCreateAPIView.as_view(),
           name="examplemodel-list-create",
       ),
       # GET(id), PUT(id), PATCH(id), DELETE(id)
       path(
           "examplemodel/<int:pk>/",
           ExampleModelRetrieveUpdateDestroyAPIView.as_view(),
           name="examplemodel-detail",
       ),
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

4. コンテナを起動して、`/swagger/`で CRUD の挙動を確認する。
