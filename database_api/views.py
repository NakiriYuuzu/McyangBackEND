from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Course, Course_Record, Teacher, Student, Sign, Race_Answer, Race_List, Sign_Record, Team_Desc, \
    Team, Team_Member, QA_Topic, Question, Answer_Member
from .serializer import CourseSerializer, StudentSerializer, SignSerializer, \
    Race_AnswerSerializer, Race_ListSerializer, Sign_RecordSerializer, Team_DescSerializer, TeamSerializer, \
    Team_MemberSerializer, Course_RecordSerializer, QA_TopicSerializer, QuestionSerializer, Answer_MemberSerializer, \
    TeacherSerializer


# bg1.老師登入
@csrf_exempt
def login(request):
    return render(request, 'login.html', {})


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            if Teacher.objects.filter(T_Email=email, T_Password=password).exists():
                return render(request, 'index.html', {})
            else:
                print("Email OR Password Error! Please try again!!!!")
                return redirect('/')
        except Exception as identifier:
            print("Exception!!!!")
            return redirect('/')
    else:
        print("Method IS NOT POST!!!!")
        return render(request, 'login.html', {})


@csrf_exempt
def student_login(request):
    email = request.POST.get('S_Email')
    password = request.POST.get('S_Password')
    data = {}

    print(email, password)

    if Student.objects.filter(S_Email=email, S_Password=password).exists():
        data['status'] = True
        data['S_id'] = Student.objects.get(S_Email=email, S_Password=password).S_id
        data['S_Name'] = Student.objects.get(S_Email=email).S_Name
        response = JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False}, status=status.HTTP_200_OK)
    else:
        response = JsonResponse({'status': "帳號或密碼錯誤！"}, safe=False, json_dumps_params={'ensure_ascii': False},
                                status=status.HTTP_400_BAD_REQUEST)

    return response


@csrf_exempt
def show_course(request):
    student_id = request.POST.get('S_id')
    list_json = []

    if student_id:
        raw = Course.objects.raw('select DISTINCT course.*, teacher.T_Name ' +
                                 'from course ' +
                                 'left join course_record on course.C_id = course_record.C_id_id ' +
                                 'left join teacher on course.T_id_id = teacher.T_id ' +
                                 'where course_record.S_id_id = %s', [student_id])
        for result in raw:
            list_json.append({'C_id': result.C_id, 'C_Name': result.C_Name, 'T_Name': result.T_Name})

    else:
        list_json.append({"status": False})

    return JsonResponse(list_json, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def show_sign_course(request):
    sign_id = request.GET.get('id', '')
    data = []
    sql = 'select T_Name, C_Name, Sign_id from sign left join course on sign.C_id_id = course.C_id left join teacher on teacher.T_id = course.T_id_id'

    if sign_id:
        raw = Sign.objects.raw(sql + ' where Sign_id = %s', [sign_id])
        for result in raw:
            data.append({'T_Name': result.T_Name, 'C_Name': result.C_Name, 'Sign_id': result.Sign_id})
    else:
        raw = Sign.objects.raw(sql)
        for result in raw:
            data.append({'T_Name': result.T_Name, 'C_Name': result.C_Name, 'Sign_id': result.Sign_id})

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


@csrf_exempt
def course_sign(request):
    student_id = request.POST.get('S_id')
    sign_id = request.POST.get('Sign_id')
    data = {}
    course_arr = []
    in_course = ""

    print(request.POST)

    # 簽到過了沒有
    raw = Sign_Record.objects.raw('select sr.* from sign_record sr '
                                  'inner join sign s on sr.Sign_id_id = s.Sign_id '
                                  'inner join student st on sr.S_id_id = st.S_id '
                                  'inner join course c on s.C_id_id = c.C_id '
                                  'where sr.S_id_id = %s and sr.Sign_id_id = %s', [student_id, sign_id])

    student_check = Course.objects.raw('select c.* from course c '
                                       'left join course_record cr on cr.C_id_id = c.C_id '
                                       'left join student st on st.S_id = cr.S_id_id '
                                       'where S_id = %s', [student_id])

    course_check = Sign.objects.raw('select * from sign where Sign_id = %s', [sign_id])

    for result in student_check:
        course_arr.append(result.C_id)

    for result in course_check:
        in_course = result.C_id_id

    if student_id and sign_id:
        if in_course not in course_arr:
            data["status"] = False
            data["message"] = "您不在此課程，請通知老師把你加入該課程!"

        elif len(raw) == 0:
            Sign_Record.objects.create(S_id_id=student_id, Sign_id_id=sign_id)
            data["status"] = True
            data["message"] = "簽到成功！"

        else:
            data["status"] = False
            data["message"] = "您已經簽到過了！"

    else:
        data["status"] = False
        data["message"] = "無法簽到...缺乏資料..."

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


# Rest Framework API ##################################################################################################

# 3.CourseAPI 老師課程查詢&創建課程
class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    lookup_field = 'T_id'

    # 1
    def get_queryset(self):
        if 'T_id' in self.kwargs:
            return Course.objects.filter(T_id=self.kwargs['T_id'])
        else:
            return Course.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


# 4.Sign 老師開始點名&學生簽到
class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

    lookup_field = 'S_id'

    def get(self, request, S_id):
        if S_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)


# 4.Sign 老師開始點名&學生簽到
class TeacherViewSet(ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

    lookup_field = 'T_id'

    def get(self, request, T_id):
        if T_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)


class CourseRecordViewSet(ModelViewSet):
    serializer_class = Course_RecordSerializer
    queryset = Course_Record.objects.all()

    lookup_field = 'CR_id'

    def get(self, request, CR_id):
        if CR_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)


class SignViewSet(ModelViewSet):
    serializer_class = SignSerializer
    queryset = Sign.objects.all()

    lookup_field = 'Sign_id'

    def get(self, request, Sign_id):
        return self.list(request)


class SignRecordViewSet(ModelViewSet):
    serializer_class = Sign_RecordSerializer
    queryset = Sign_Record.objects.all()

    lookup_field = 'Sign_id'

    def get_queryset(self):
        if 'Sign_id' in self.kwargs:
            return Sign_Record.objects.filter(Sign_id=self.kwargs['Sign_id'])
        else:
            return Sign_Record.objects.all()

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


# 5.Race_Answer 老師開放搶答&學生開始搶答
class Race_AnswerViewSet(ModelViewSet):
    serializer_class = Race_AnswerSerializer
    queryset = Race_Answer.objects.all()

    lookup_field = 'R_id'

    def get(self, request, R_id):
        if R_id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def update(self, request, R_id):
        stu = Race_Answer.objects.get(R_id=R_id)
        serializer = Race_AnswerSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def post(self, request):
        return self.create(request)


class Race_ListViewSet(ModelViewSet):
    serializer_class = Race_ListSerializer
    queryset = Race_List.objects.all()

    lookup_field = 'id'

    def get_queryset(self):
        if 'id' in self.kwargs:
            return Race_List.objects.filter(id=self.kwargs['id'])
        else:
            return Race_List.objects.all()

    def update(self, request, id):
        stu = Race_List.objects.get(id=id)
        serializer = Race_ListSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


class Race_List_R_ViewSet(ModelViewSet):
    serializer_class = Race_ListSerializer
    queryset = Race_List.objects.all()

    lookup_field = 'R_id'

    def get_queryset(self):
        if 'R_id' in self.kwargs:
            return Race_List.objects.filter(R_id=self.kwargs['R_id'])
        else:
            return Race_List.objects.all()

    def update(self, request, R_id):
        stu = Race_List.objects.get(R_id=R_id)
        serializer = Race_ListSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


# 6.Team_老師發放隊長跟組員組隊訊號
class Team_DescViewSet(ModelViewSet):
    serializer_class = Team_DescSerializer
    queryset = Team_Desc.objects.all()

    lookup_field = 'C_id'

    def get_queryset(self):
        if 'C_id' in self.kwargs:
            return Team_Desc.objects.filter(C_id=self.kwargs['C_id'])
        else:
            return Team_Desc.objects.all()

    def update(self, request, C_id):
        stu = Team_Desc.objects.get(C_id=C_id)
        serializer = Team_DescSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


# 組員新增
class TeamLeaderViewSet(ModelViewSet):
    serializer_class = Team_DescSerializer
    queryset = Team.objects.all()

    lookup_field = 'Group_limit'


class TeamViewSet(ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    lookup_field = 'Team_id'

    def get_queryset(self):
        if 'Team_id' in self.kwargs:
            return Team.objects.filter(Team_id=self.kwargs['Team_id'])
        else:
            return Team.objects.all()

    def update(self, request, Team_id):
        stu = Team.objects.get(Team_id=Team_id)
        serializer = TeamSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


class Team_MemberViewSet(ModelViewSet):
    serializer_class = Team_MemberSerializer
    queryset = Team_Member.objects.all()

    lookup_field = 'TeamMember_id'

    def get_queryset(self):
        if 'TeamMember_id' in self.kwargs:
            return Team_Member.objects.filter(TeamMember_id=self.kwargs['TeamMember_id'])
        else:
            return Team_Member.objects.all()

    def update(self, request, TeamMember_id):
        stu = Team_Member.objects.get(TeamMember_id=TeamMember_id)
        serializer = Team_MemberSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


# 7.QA_老師開始提問跟學生答題
class QA_TopicViewSet(ModelViewSet):
    serializer_class = QA_TopicSerializer
    queryset = QA_Topic.objects.all()

    lookup_field = 'C_id'

    def get_queryset(self):
        if 'C_id' in self.kwargs:
            return QA_Topic.objects.filter(C_id=self.kwargs['C_id'])
        else:
            return QA_Topic.objects.all()

    def update(self, request, C_id):
        stu = QA_Topic.objects.get(C_id=C_id)
        serializer = QA_TopicSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    lookup_field = 'QA_id'

    def get_queryset(self):
        if 'QA_id' in self.kwargs:
            return Question.objects.filter(QA_id=self.kwargs['QA_id'])
        else:
            return Question.objects.all()

    def update(self, request, QA_id):
        stu = Question.objects.get(QA_id=QA_id)
        serializer = QuestionSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


class Question_QViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    lookup_field = 'Q_id'

    def get_queryset(self):
        if 'Q_id' in self.kwargs:
            return Question.objects.filter(Q_id=self.kwargs['Q_id'])
        else:
            return Question.objects.all()

    def update(self, request, Q_id):
        stu = Question.objects.get(Q_id=Q_id)
        serializer = QuestionSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)


class Answer_MemberViewSet(ModelViewSet):
    serializer_class = Answer_MemberSerializer
    queryset = Answer_Member.objects.all()

    lookup_field = 'Answer_id'

    def get_queryset(self):
        if 'Answer_id' in self.kwargs:
            return Answer_Member.objects.filter(Answer_id=self.kwargs['Answer_id'])
        else:
            return Answer_Member.objects.all()

    def update(self, request, Answer_id):
        stu = Answer_Member.objects.get(Answer_id=Answer_id)
        serializer = Answer_MemberSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return self.retrieve(request)

    def retrieve(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def post(self, request):
        return self.create(request)
