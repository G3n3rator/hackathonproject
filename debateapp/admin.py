from django.contrib import admin
# CustomUserをインポート
from .models import AgendaPost, DebateMessage

class AgendaPostAdmin(admin.ModelAdmin):
    '''
    管理者ページのレコード一覧に表示するカラムを設定するクラス
    '''
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

class DebateMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_pk')
    list_display_links = ('id', 'room_pk')

# Django管理者サイトにAgenda, AgendaPostAdminを登録する
admin.site.register(AgendaPost, AgendaPostAdmin)
admin.site.register(DebateMessage, DebateMessageAdmin)
