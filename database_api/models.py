from django.db import models


# Create your models here.
# 資料庫中創建字段
class Teacher(models.Model):
    T_id = models.AutoField(primary_key=True)
    T_Name = models.TextField(max_length=30)
    T_Email = models.TextField(max_length=50, unique=True)
    T_Password = models.TextField(max_length=50)

    class Meta:
        unique_together = (('T_id', 'T_Email'),)
        db_table = 'teacher'


class Student(models.Model):
    S_id = models.AutoField(primary_key=True)
    S_Name = models.TextField(max_length=30)
    S_Email = models.TextField(max_length=50, unique=True)
    S_Password = models.TextField(max_length=50)

    class Meta:
        db_table = 'student'


# 課程
class Course(models.Model):
    C_id = models.AutoField(primary_key=True)
    T_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, to_field="T_id")
    C_Name = models.TextField(max_length=30)

    class Meta:
        db_table = 'course'


# 修課紀錄
class Course_Record(models.Model):
    CR_id = models.AutoField(primary_key=True)
    C_id = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="C_id")
    S_id = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="S_id")

    class Meta:
        db_table = 'course_record'


class Race_Answer(models.Model):
    R_id = models.AutoField(primary_key=True)
    C_id = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="C_id")
    Race_doc = models.TextField(max_length=255, unique=True)
    Status = models.BooleanField(default=True)
    Time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'race_answer'


class Race_List(models.Model):
    R_id = models.ForeignKey(Race_Answer, on_delete=models.CASCADE, to_field="R_id")
    S_id = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="S_id")  # 搶答的學生
    Answer = models.BooleanField(default=True)  # 搶答正確的學生
    Time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'race_list'


# 點名單
class Sign(models.Model):
    Sign_id = models.AutoField(primary_key=True)
    C_id = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="C_id")
    Time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sign'


# 紀錄有簽到的學生
class Sign_Record(models.Model):
    SR_id = models.AutoField(primary_key=True)
    Sign_id = models.ForeignKey(Sign, on_delete=models.CASCADE, to_field="Sign_id")
    S_id = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="S_id")
    Time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sign_record'


class Team_Desc(models.Model):
    TeamDesc_id = models.AutoField(primary_key=True)
    Team_doc = models.TextField(max_length=255)
    Group_Total = models.IntegerField()
    Group_limit = models.IntegerField()
    C_id = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="C_id")
    Time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team_desc'


class Team(models.Model):
    Team_id = models.AutoField(primary_key=True)
    Team_desc = models.ForeignKey(Team_Desc, on_delete=models.CASCADE, to_field="TeamDesc_id")
    Group_number = models.IntegerField()
    Leader_id = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        db_table = 'team'


class Team_Member(models.Model):
    TeamMember_id = models.AutoField(primary_key=True)
    S_id = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="S_id")
    Team_id = models.ForeignKey(Team, on_delete=models.CASCADE, to_field="Team_id")
    Time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'team_member'


class QA_Topic(models.Model):
    QA_id = models.AutoField(primary_key=True)
    QA_doc = models.TextField(max_length=255)
    C_id = models.ForeignKey(Course, on_delete=models.CASCADE, to_field="C_id")

    class Meta:
        db_table = 'qa_topic'


class Question(models.Model):
    Q_id = models.AutoField(primary_key=True)
    QA_id = models.ForeignKey(QA_Topic, on_delete=models.CASCADE, to_field="QA_id")
    Q_doc = models.TextField(max_length=255)

    class Meta:
        db_table = 'question'


class Answer_Member(models.Model):
    Answer_id = models.AutoField(primary_key=True)
    Q_id = models.ForeignKey(Question, on_delete=models.CASCADE, to_field="Q_id")
    S_id = models.ForeignKey(Student, on_delete=models.CASCADE, to_field="S_id")
    Answer_doc = models.TextField(max_length=255)
    Answer = models.BooleanField(default=True)  # 回答正確的學生

    class Meta:
        db_table = 'answer_member'


class Mobile_Status(models.Model):
    id = models.AutoField(primary_key=True)
    version = models.IntegerField()

