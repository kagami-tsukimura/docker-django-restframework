import random

import requests
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloWorldAPIView(APIView):
    def get(self, request):
        return Response({"message": "Hello World"})


class JSONPlaceholderAPIView(APIView):
    def get(self, request):
        # JSONPlaceholderのAPIからデータを取得
        response = requests.get("https://jsonplaceholder.typicode.com/todos")
        todos = response.json()
        data = random.choice(todos)
        return Response(data)
