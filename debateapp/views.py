from django.shortcuts import render
# ListViewは文字通りリスト表示するビュー
from django.views.generic import TemplateView, ListView
# 投稿のためにCreateViewをインポート
from django.views.generic import CreateView
# 詳細表示のためにDetailViewをインポート(これを使って討論する部屋をつくる)
from django.views.generic import DetailView
# urlパターンではなくビューから名前で解決するためにreverse_lazyを使用
from django.urls import reverse_lazy
from .forms import AgendaPostForm
from .models import AgendaPost
# アクセスをログインユーザーに制限するためのデコレーターをインポート
from django.utils.decorators import method_decorator
# ログインしていないユーザーをログインページに飛ばす
from django.contrib.auth.decorators import login_required
# .envファイル読み込むためのload_dotenvをインポート(読み込み時load_env()を使用)
from dotenv import load_dotenv
# csrfチェックをスキップするもの(これについてはセキュリティ的に要検討)
from django.views.decorators.csrf import csrf_exempt
# jsonデータを取り扱うため
import json
# 環境変数を読み込むため
import os
from django.http import JsonResponse
import requests
from .models import DebateMessage
from accountsapp.models import CustomUser
from asgiref.sync import sync_to_async
import logging
class IndexView(ListView):
    '''
    トップページのビュー
    '''
    template_name = 'index.html'
    # モデルPostAgendaのオブジェクトにorder_by()を適用して、投稿日時の降順(-)で並べ替える
    queryset = AgendaPost.objects.order_by('-posted_at')

# デコレーターにより、CreateAgendaViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreateAgendaView(CreateView):
    form_class = AgendaPostForm
    template_name = "post_agenda.html"
    success_url = reverse_lazy('debateapp:post_done')

    def form_valid(self, form):
        '''
        CreateViewクラスのform_validをオーバーライト

        フォームのバリデーションを通過した時に呼ばれる
        フォームデータの登録をここで行う
        '''
        # 入力されたデータを加工する(ここではユーザーidを加える)ため、ここではcommit=Falseとしておく。
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに格納
        postdata.save()
        # 戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)
    
class PostSuccessView(TemplateView):
    template_name = 'post_success.html'

@method_decorator(login_required, name='dispatch')
class DebateRoomView(DetailView):
    template_name = 'debate_room.html'
    model = AgendaPost

# 環境変数読み込み
load_dotenv()
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv("DIFY_API_URL")
# DIFY_API_KEY2 = os.getenv("DIFY_API_URL2")
# DIFY_API_KEY2 = os.getenv("DIFY_API_KEY2")
@csrf_exempt
def dify_proxy(request):
    if request.method != "POST":
        return JsonResponse({"error":"Method not allowed"}, status=405)
    
    data = json.loads(request.body)
    message = data.get("message", "")

    # Difyへの問い合わせ
    if not message:
        return JsonResponse({"error":"Empty message"}, status=400)
    try:
        response = requests.post(
            DIFY_API_URL,
            headers={
                "Authorization":f"Bearer {DIFY_API_KEY}",
                "Content-Type":"application/json"
            },
            json = {
                "inputs":{"message":message},
                "query":'ここまでの発言内容がパラグラフライティングで書かれていて、かつ、筋が通っている場合は"YES"と返事してください。それ以外は"NO"と返事してください。',
                "user":"abc-123",
                "response_mode":"blocking"
            }
        )
        response.raise_for_status() # HTTPエラーチェック
        answer = response.json().get("answer","").strip().upper()
        # print(answer)
        return JsonResponse({"answer":answer})
    # エラー発生したら、エラーの内容出力
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error":str(e)}, status=500)

    # ボットメッセージ保存(今後実装)

# メッセージ保存
# csrf免除については今後検討
@csrf_exempt
def save_message(request, pk):
    if request.method != "POST":
        return JsonResponse({"error":"Method not allowed"}, status=405)
    try:
        data = json.loads(request.body)
        message = data.get("message", "")
        username = data.get("username", "")
        user = CustomUser.objects.get(username=username)
        messages = DebateMessage.objects.filter(room_pk=pk).order_by("timestamp")
        # レコード数が20以上であれば保存拒否
        if messages.count() >= 20:
            return JsonResponse({"error":"この討論空間は既に上限である20個の発言がされました。"})
        # 保存処理
        DebateMessage.objects.create(
        username=user,
        room_pk=pk,
        message=message
        )
        # 要約&優れた発言
        messages = DebateMessage.objects.filter(room_pk=pk).order_by("timestamp")
        if messages.count() == 20:
            # logging.debug('debug message')
            history = "\n".join([f"{m.username}:{m.message}" for m in messages])
            response = requests.post(
                DIFY_API_URL,
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}",
                    "Content-Type":"application/json"
                },
                json ={
                    "inputs":{"history":history},
                    "response_mode":"blocking",
                    "query":"ここまでの情報は'発言者':'メッセージ'というフォーマットの会話なので、この討論の全体のまとめと一番良かったと思う発言について語ってください。",
                    "user": "abc-123"
                }
            )
            answer = response.json().get("answer","").strip().upper()
            # print(answer)
            return JsonResponse({"answer":answer})
        return JsonResponse({"status":"OK"})
    # エラー発生したら、エラーの内容出力
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error":str(e)}, status=500)
