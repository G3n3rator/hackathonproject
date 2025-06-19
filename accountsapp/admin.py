from django.contrib import admin

# CustomUserをインポート
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    '''
    管理者ページのレコード一覧に表示するカラムを設定するクラス
    '''
    # レコード一覧にidとusernameを表示する
    list_display = ('id', 'username')
    # 表示するカラムにリンクを設定
    list_display_links = ('id', 'username')

# Djang管理者サイトにCustomUser, CustomUserAdminを登録する
admin.site.register(CustomUser, CustomUserAdmin)
