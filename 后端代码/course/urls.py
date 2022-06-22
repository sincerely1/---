from .views import *
from django.urls import path
urlpatterns = [
    path('courses/',GetCourses.as_view(),name='courses'),
    path('addcourse/',AddCourseView.as_view(),name='add_course'),
    path('delcourse/',DelCourseView.as_view(),name='del_course'),
    path('select/', GetSelectCourse.as_view(), name='select_course'),
    path('delselect/',DelSelectCourseView.as_view(),name='del_select'),
    path('notselect/',GetNotSelectCourseView.as_view(),name='not_select_course'),
    path('addselect/',AddSelectCourseView.as_view(),name='add_select_course'),
    path('demodownload/',DownloadDemo.as_view(), name='download_demo'),
    path('uploadinfo/',GetUplodInfo.as_view(), name='get_upload_info'),
    path('uploaddata/',UploadFileView.as_view(),name='upload_data'),
    path('deletedata/', DeleteDataView.as_view(), name='delete_data'),
    path('analysisdata/', AnalysisView.as_view(), name='analysis_data'),
    path('exportdata/', ExportAnalysisData.as_view(), name='export_data'),
]
