from rest_framework import serializers
from authapp.models import Users
from projectsapp.models import Project, ProjectDiscussItem, ProjectManagers, ProjectImage, ProjectHasTechnicalSolutions, \
    ProjectCompany


class ProjectCompaniesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectCompany
        fields = '__all__'


class ProjectSolutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectHasTechnicalSolutions
        fields = '__all__'


class ProjectImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = '__all__'


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class ProjectCommentSerializer(serializers.ModelSerializer):
    user = CommentAuthorSerializer(many=False, read_only=True)

    class Meta:
        model = ProjectDiscussItem
        fields = '__all__'


class CommentCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ProjectDiscussItem
        fields = '__all__'


class ProjectManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectManagers
        fields = '__all__'


class ProjectDetailSerializer(serializers.ModelSerializer):
    managers = ProjectManagerSerializer(many=True, read_only=True)
    comments = ProjectCommentSerializer(many=True, read_only=True)
    images = ProjectImagesSerializer(many=True, read_only=True)
    solutions = ProjectSolutionsSerializer(many=True, read_only=True)
    companies = ProjectCompaniesSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('pk', 'name', 'image', 'creation_date', 'city', 'status')
