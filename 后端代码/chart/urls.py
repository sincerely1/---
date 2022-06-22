from django.urls import path
from .views import *

urlpatterns = [
    path('has_analysis_course/', GetHasAnalysisView.as_view(), name='as_analysis'),
    path('knowledge_commit/', GetKnowledgeCommit.as_view(), name='knowledge_commit'),
    path('knowledge_first_accept/', GetKnowledgeFirstAccept.as_view(), name='knowledge_commit'),
    path('knowledge_pass/', GetKnowledgePass.as_view(), name='knowledge_commit'),
    path('return_data/', GetKnowledgeReturnInfo.as_view(), name='return_data'),
    path('level_accept_data/', GetLevelAcceptInfo.as_view(), name='leve_accept_data'),
    path('level_commit_data/', GetLevelCommitInfo.as_view(), name='leve_commit_data'),
    path('level_code_data/', GetLevelCodeInfo.as_view(), name='leve_code_data'),
    path('question_type_data/', GetQuestionTypeInfo.as_view(), name='leve_code_data'),
    path('student_dashboard_data/', GetStudentDashboardInfo.as_view(), name='stu_dashboard'),
    path('teacher_start_commit/', GetStudentStartCommit.as_view(), name='start_commit'),
    path('return_sum_data/', GetReturnSumInfo.as_view(), name='return_data'),
    path('ability_count_data/', GetAbilitySumInfo.as_view(), name='ability_count'),
    path('knowledge_summary_data/', GetKnowledgeSummaryInfo.as_view(), name='knowledge_summary'),
    path('level_summary_data/', GetLevelSummaryInfo.as_view(), name='level_summary'),
    path('type_summary_data/', GetTypeSummaryInfo.as_view(), name='type_summary'),
    path('teacher_dashboard_data/', GetTeacherDashboardInfo.as_view(), name='teacher_dashboard'),
    path('teacher_compare_data/', GetTeacherCompareInfo.as_view(), name='teacher_compare'),
    path('teacher_homework_commit/', GetHomeworkCommitInfo.as_view(), name='teacher_homework_commit'),
]
