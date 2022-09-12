from rest_framework import serializers

from core import models


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User 
        fields = ['id', 'username', 'email']


class ProjectSerializer(serializers.ModelSerializer):

    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Project
        fields = ['id', 'title', 'description', 
                  'members', 'owner', 'is_active', 'updated_at', 'created_at']
        
        read_only_fields = ['updated_at', 'created_at']


class CreateTaskSerializer(serializers.ModelSerializer):

    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    assignees = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Task
        fields = ['id', 'project', 'title', 
                  'description', 'status', 'assignees', 
                  'author', 'updated_at', 'created_at']
        
        read_only_fields = ['updated_at', 'created_at']


    def validate(self, data):
        is_pm = self.context.get('request').user.projects \
                .filter(pk=data['project'].id).exists()

        is_member = self.context.get('request').user.assigned_projects \
                    .filter(pk=data['project'].id).exists()

        if not is_pm and not is_member:
            raise serializers.ValidationError("Project not found")

        if is_member and not is_pm:
            data['assignees'] = [self.context.get('request').user]

        for assignee in data['assignees']:
            if assignee == self.context.get('request').user:
                continue

            assignee_pm_role = assignee.projects.filter(pk=data['project'].id).exists()
            assignee_member_role = assignee.assigned_projects.filter(pk=data['project'].id).exists()

            if not assignee_pm_role and not assignee_member_role:
                raise serializers.ValidationError(
                        f"{assignee.username} is not a collaborator of the provided project."
                    )

        return super().validate(data)


class UpdateTaskSerializer(serializers.ModelSerializer):

    assignees = serializers.SlugRelatedField(
        many=True,
        slug_field='username',
        queryset=models.User.objects.all()
    )

    class Meta:
        model = models.Task
        fields = ['id', 'author', 'project', 'title', 
                  'description', 'status', 'assignees', 
                  'updated_at', 'created_at']
        
        read_only_fields = ['author', 'updated_at', 'created_at']


    def update(self, instance, validated_data):
        if 'project' in validated_data:
            validated_data.pop('project', None)
            
        return super().update(instance, validated_data)

    def validate(self, data):
        is_pm = self.context.get('request').user.projects \
                .filter(pk=data['project'].id).exists()

        is_member = self.context.get('request').user.assigned_projects \
                    .filter(pk=data['project'].id).exists()

        if not is_pm and not is_member:
            raise serializers.ValidationError("Project not found")

        if is_member and not is_pm:
            data.pop('assignees', None)
        else:
            for assignee in data['assignees']:
                if assignee == self.context.get('request').user:
                    continue

                assignee_pm_role = assignee.projects.filter(pk=data['project'].id).exists()
                assignee_member_role = assignee.assigned_projects.filter(pk=data['project'].id).exists()

                if not assignee_pm_role and not assignee_member_role:
                    raise serializers.ValidationError(
                            f"{assignee.username} is not a collaborator of the provided project."
                        )

        return super().validate(data)


class ReadTaskSerializer(serializers.ModelSerializer):

    author = AuthorSerializer()
    assignees = AuthorSerializer(many=True)

    class Meta:
        model = models.Task
        fields = ['id', 'project', 'title', 
                  'description', 'status', 'assignees', 
                  'author', 'updated_at', 'created_at']

        read_only_fields = fields