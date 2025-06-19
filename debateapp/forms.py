from django.forms import ModelForm
from .models import AgendaPost

class AgendaPostForm(ModelForm):
    '''
    ModelFormのサブクラス(継承)
    '''
    class Meta:
        '''
        ModelFormのインナークラス(改造)
            model:モデルのクラス
            fields:フォームで使用するモデルのフィールドを指定
        '''
        model = AgendaPost
        fields = ['title', 'comment']
