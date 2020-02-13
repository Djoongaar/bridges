from rest_framework import serializers

from authapp.models import Users
from newsapp.models import News, NewsDiscussItem, NewsProduct


class NewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        exclude = ["slug", "status"]


class NewsCommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'avatar', 'social_media_image']


class NewsCommentsSerializer(serializers.ModelSerializer):
    user = NewsCommentAuthorSerializer(many=False, read_only=True)

    class Meta:
        model = NewsDiscussItem
        fields = '__all__'


class NewsProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsProduct
        fields = '__all__'


class NewsDetailSerializer(serializers.ModelSerializer):
    comments = NewsCommentsSerializer(many=True, read_only=True)
    solutions = NewsProductSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'
