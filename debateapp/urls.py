from django.urls import path
from . import views
# ビューじゃないものの場合はこう記述する必要があるようだ
from .views import dify_proxy, save_message

# URLパターン逆引き
app_name = 'debateapp'

# URLパターンを登録する変数
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post_agenda/', views.CreateAgendaView.as_view(), name='post_agenda'),
    path('post_done/', views.PostSuccessView.as_view(), name='post_done'),
    # pkを受け取ってオブジェクトを判断する
    path('debate_room/<int:pk>', views.DebateRoomView.as_view(), name='debate_room'),
    path('api/check_message/', dify_proxy),
    path('save-message/<int:pk>', save_message),
    #以下池川による改変
    path('threads/search/', views.thread_search, name='thread_search'),
]
