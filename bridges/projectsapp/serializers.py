from rest_framework import serializers
from projectsapp.models import Project, ProjectDiscussItem


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('pk', 'name', 'image', 'creation_date', 'city', 'status')


class ProjectCommentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProjectDiscussItem
        fields = '__all__'
