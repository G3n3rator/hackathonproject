from django.db import models
# accountsappのmodelsからCustomUserをインポート
from accountsapp.models import CustomUser

class AgendaPost(models.Model):
    user = models.ForeignKey(
        # CustomUserを親とする外部キー
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # ユーザーを削除する場合はそのユーザーの投稿データもすべて削除する
        on_delete=models.CASCADE
        )
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
        )
    comment = models.TextField(
        verbose_name='コメント'
        )
    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True # 日時を自動追加
        )
    def __str__(self):
        '''
        オブジェクトをstrに変換して返す
        return (投稿した議題のタイトル)
        '''
        return self.title

class DebateMessage(models.Model):
    room_pk = models.BigIntegerField()
    username = models.ForeignKey(
        # CustomUserを親とする外部キー
        CustomUser,
        # フィールドのタイトル
        verbose_name='ユーザー',
        # データの整合性のため、一応データは残るようにする
        on_delete=models.PROTECT
    )
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __int__(self):
        return self.room_pk
