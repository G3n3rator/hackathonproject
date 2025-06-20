from django.shortcuts import render
from django.views.generic import CreateView, TemplateView
from .forms import CustomUserCreationForm
# reverse_lazy()でクラスビュー内でURLを名前で解決する
from django.urls import reverse_lazy

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy('accountsapp:signup_success')

    def form_valid(self, form):
        # フォームに入力されたものを変数userに渡す
        user = form.save()
        # モデルに保存
        self.object = user
        # 戻り地はスーパークラス(親クラスのメソッド呼び出し)のform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)

class SignUpSuccessView(TemplateView):
    template_name = "signup_success.html"

