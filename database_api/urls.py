from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views
from .views import *

router = DefaultRouter()
router.register('Student', StudentViewSet)
router.register('teacher', TeacherViewSet)
router.register('CourseCreate', CourseViewSet)
router.register('CourseRecord', CourseRecordViewSet)
router.register('Sign', SignViewSet)
router.register('SignRecord', SignRecordViewSet)
router.register('Race_List', Race_ListViewSet)
router.register('Race_Answer', Race_AnswerViewSet)
router.register('Race_List_R', Race_List_R_ViewSet)
router.register('Team_Desc', Team_DescViewSet)
router.register('Team', TeamViewSet)
router.register('Team_Member', Team_MemberViewSet)
router.register('QA_Topic', QA_TopicViewSet)
router.register('Question', QuestionViewSet)
router.register('Question_Q', Question_QViewSet)
router.register('Answer_Member', Answer_MemberViewSet)

urlpatterns = [

    path('api/', include(router.urls)),
    path('api/studentLogin/', student_login),
    path('api/showCourse/', show_course),
    path('api/courseSigned/', course_sign),
    path('api/listSignCourse/', show_sign_course),

    # 後臺網頁
    path('', views.login, name="login"),
    path('user_login/', views.user_login, name="user_login"),

]
