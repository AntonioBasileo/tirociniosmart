from django.contrib.auth.models import User
from rest_framework import serializers
from app.model.training_models import AppUser, Company, Training


class AppUserToDTO(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = AppUser
        fields = ['username', 'email']

class AppUserToEntity(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = AppUser
        fields = ['username', 'password', 'email']

    def validate(self, validated_data):
        email = validated_data.get('email', None)

        if not AppUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not found")

        password = validated_data.get('password', None)

        if password is None or password == "":
            raise serializers.ValidationError("Password is required")

        return validated_data

    def create(self, validated_data):
        return AppUser(**validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        return instance

class CompanyToDTO(serializers.ModelSerializer):
    name = serializers.CharField(source='company.name', read_only=True)
    phoneNumber = serializers.CharField(source='company.phoneNumber', read_only=True)
    email = serializers.CharField(source='company.email', read_only=True)
    address = serializers.CharField(source='company.address', read_only=True)

    class Meta:
        model = AppUser
        fields = ['name', 'phoneNumber', 'email', 'address']

class CompanyToEntity(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = '__all__'

    def validate(self, validated_data):
        return validated_data

    def create(self, validated_data):
        return Company(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
        instance.email = validated_data.get('email', instance.email)
        instance.address = validated_data.get('address', instance.address)
        instance.save()

        return instance

class TrainingToDTO(serializers.ModelSerializer):
    request_date = serializers.DateTimeField(read_only=True)
    limit_acceptance_date = serializers.DateTimeField(read_only=True)
    date_start = serializers.DateField(read_only=True)
    date_end = serializers.DateField(read_only=True)
    accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Company
        fields = ['request_date', 'limit_acceptance_date', 'date_start', 'date_end', 'accepted']

class TrainingToEntity(serializers.ModelSerializer):
    limit_acceptance_date = serializers.DateTimeField()
    date_start = serializers.DateField()
    date_end = serializers.DateField()
    user_id = serializers.IntegerField(write_only=True)
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Company
        fields = ['limit_acceptance_date', 'date_start', 'date_end', 'user_id', 'company_id']

    def validate(self, validated_data):
        if validated_data.get('date_end') > validated_data.get('date_start'):
            raise serializers.ValidationError("date_end cannot be greater than date_start")

        if validated_data.get('limit_acceptance_date') < validated_data.get('date_end'):
            raise serializers.ValidationError("date_end cannot be greater than limit_acceptance_date")

        if validated_data.get('user_id') is None or User.objects.filter(id=validated_data.get('user_id')).exists() is False:
            raise serializers.ValidationError("User not found")

        if validated_data.get('company_id') is None or Company.objects.filter(id=validated_data.get('company_id')).exists() is False:
            raise serializers.ValidationError("Company not found")

        return validated_data

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        company_id = validated_data.pop('company_id')
        validated_data['user'] = AppUser.objects.get(id=user_id)
        validated_data['company'] = Company.objects.get(id=company_id)

        return Training(**validated_data)

    def update(self, instance, validated_data):
        instance.limit_acceptance_date = validated_data.get('limit_acceptance_date', instance.limit_acceptance_date)
        instance.date_start = validated_data.get('date_start', instance.date_start)
        instance.date_end = validated_data.get('date_end', instance.date_end)
        instance.save()

        return instance

class TrainingRegisterDTO(serializers.Serializer):
    description = serializers.CharField(read_only=True)