from django.urls import path
import my_info.views as info_views

app_name = 'my_info'

urlpatterns = [
    path('login/', info_views.login, name='login'),
    path('', info_views.index, name='index'),
    path('help/', info_views.help, name='help'),
    path('log/', info_views.log, name='log'),
    path('grade/', info_views.grade, name='grade'),
    path('logout/', info_views.logout, name='logout'),
    path('api/', info_views.api, name='api'),
    path('work/', info_views.work, name='work'),
    path('work_detail/<int:work_id>/', info_views.word_detail, name='work_detail'),
    path('topic_api/',info_views.topic_api,name='topic_api'),
    path('work_result/',info_views.work_result,name='work_result'),
    path('work_result_detail/<int:work_id>/',info_views.work_result_detail,name='work_result_detail'),
]
