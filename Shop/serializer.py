from dataclasses import fields
from rest_framework import serializers
from .models import Cart, Product

'''
class postSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    content = serializers.CharField(style={'base_template': 'textarea.html'})# for text fields
    date_posted = serializers.DateTimeField()
    author = serializers.IntegerField()
'''


class productSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class cartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = "__all__"