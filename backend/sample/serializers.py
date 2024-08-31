from rest_framework import serializers

from .models import AreaMaster, ExampleModel


class ExampleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExampleModel
        fields = "__all__"  # モデルの全てのフィールドをシリアライズ


class AreaMasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaMaster
        fields = "__all__"  # モデルの全てのフィールドをシリアライズ
