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
'''
以下池川による改変
'''

class Serch(forms.Form):
    query = forms.CharField(label='検索キーワード', max_length=200, required=False)
