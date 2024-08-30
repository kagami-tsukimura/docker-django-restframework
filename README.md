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
