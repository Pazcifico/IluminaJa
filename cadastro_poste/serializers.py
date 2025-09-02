from rest_framework import serializers
from .models import Lampada, Poste


class PosteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poste
        fields = '__all__'


class LampadaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lampada
        fields = '__all__'
