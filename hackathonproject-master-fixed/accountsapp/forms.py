# ユーザー登録のためのビルトインクラス、UserCreationFormクラスをインポート
from django.contrib.auth.forms import UserCreationForm
# models.pyで定義したCustomUserモデルをインポート
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    '''
    UserCreationFormのサブクラス(継承)
    '''
    class Meta:
        '''
        UserCreationFormのインナークラス(改造)
            model:連携するUserモデル
            fields:フォームで使用するフィールド
        '''
        #連携するUserモデルを設定
        model = CustomUser
        # フォームで使用するフィールドを設定
        # ユーザー名、メールアドレス、パスワード、パスワード(確認用)
        fields = ('username', 'email', 'password1', 'password2')