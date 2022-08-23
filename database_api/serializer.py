from rest_framework import serializers
from .models import Course,Course_Record, Teacher, Student, Sign, Race_Answer, Race_List, Sign_Record,\
    Team_Desc, Team, Team_Member, QA_Topic, Question,Answer_Member


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class Course_RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course_Record
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
        # fields = ['S_id', 'S_Name']


class SignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sign
        fields = '__all__'


class Sign_RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sign_Record
        fields = '__all__'


class Race_AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race_Answer
        fields = '__all__'


class Race_ListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race_List
        fields = '__all__'


class Team_DescSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team_Desc
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class Team_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team_Member
        fields = '__all__'


class QA_TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = QA_Topic
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class Answer_MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer_Member
        fields = '__all__'
