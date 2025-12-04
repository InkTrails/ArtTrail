from django.shortcuts import render, get_object_or_404, redirect
from .models import ArtPost, UserProfile
from django.contrib.auth.models import User
from django.utils import timezone
import calendar
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

# --- 1. トップページ（ロジック改良版） ---
def index(request):
    # ▼▼▼ 1. 誰を表示するか決める ▼▼▼
    target_username = request.GET.get('user')
    display_user = None

    if target_username:
        # パターンA: 共有URL（?user=〇〇）なら、その人を表示
        display_user = get_object_or_404(User, username=target_username)
    elif request.user.is_authenticated:
        # パターンB: ログイン中なら、自分を表示
        # ★ここを修正しました！ (request.request.user → request.user)
        display_user = request.user
    else:
        # パターンC: 未ログイン＆指定なしなら、ログイン画面へ飛ばす！
        return redirect('login')
    # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

    today = timezone.now().date()

    # 年月取得
    try:
        current_year = int(request.GET.get('year', today.year))
        current_month = int(request.GET.get('month', today.month))
    except ValueError:
        current_year = today.year
        current_month = today.month

    # カレンダー計算
    first_weekday, days_in_month = calendar.monthrange(current_year, current_month)
    calendar_data = []
    empty_count = (first_weekday + 1) % 7
    for _ in range(empty_count):
        calendar_data.append({'is_empty': True})
    for day in range(1, days_in_month + 1):
        target_date = date(current_year, current_month, day)
        calendar_data.append({
            'is_empty': False,
            'date': target_date,
            'day': day,
            'count': 0,
            'color': 'bg-light text-muted'
        })

    # ▼▼▼ 2. データ取得（display_user のデータだけを取る） ▼▼▼
    # 作品リスト
    posts_list = ArtPost.objects.filter(author=display_user).order_by('-created_at')
    
    # もし「本人じゃない（他人）」が見ているなら、模写は隠す
    if request.user != display_user:
        posts_list = posts_list.filter(is_practice=False)

    # ヒートマップ用データ（本人じゃなければ公開のみカウント）
    month_logs = ArtPost.objects.filter(author=display_user, created_at__year=current_year, created_at__month=current_month)
    if request.user != display_user:
        month_logs = month_logs.filter(is_practice=False)
    # ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

    # タグ絞り込み
    tag_slug = request.GET.get('tag')
    if tag_slug:
        posts_list = posts_list.filter(tag=tag_slug)

    # ヒートマップ集計
    for log in month_logs:
        day_index = empty_count + (log.created_at.day - 1)
        calendar_data[day_index]['count'] += 1
    for data in calendar_data:
        if data.get('is_empty'): continue
        if data['count'] == 1:
            data['color'] = 'bg-info bg-opacity-25 fw-bold text-dark'
        elif data['count'] >= 2:
            data['color'] = 'bg-primary text-white fw-bold'

    # 前月・次月ボタン計算
    if current_month == 1:
        prev_year, prev_month = current_year - 1, 12
    else:
        prev_year, prev_month = current_year, current_month - 1
    if current_month == 12:
        next_year, next_month = current_year + 1, 1
    else:
        next_year, next_month = current_year, current_month + 1

    # ページネーション
    paginator = Paginator(posts_list, 12) 
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    context = {
        'display_user': display_user,
        'posts': posts,
        'calendar_data': calendar_data,
        'current_year': current_year,
        'current_month': current_month,
        'prev_year': prev_year, 'prev_month': prev_month,
        'next_year': next_year, 'next_month': next_month,
        'tag_slug': tag_slug,
    }
    return render(request, 'gallery/index.html', context)

# --- 2. 比較機能 ---
def compare(request):
    id1 = request.GET.get('id1')
    id2 = request.GET.get('id2')
    post1 = None
    post2 = None
    if id1 and id2:
        post1 = get_object_or_404(ArtPost, id=id1)
        post2 = get_object_or_404(ArtPost, id=id2)
    return render(request, 'gallery/compare.html', {'post1': post1, 'post2': post2})

# --- 3. 新規登録機能 ---
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# --- 4. 投稿機能 ---
class UploadView(LoginRequiredMixin, generic.CreateView):
    model = ArtPost
    fields = ['title', 'image', 'is_practice', 'tag']
    template_name = 'gallery/upload.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# --- 5. プロフィール編集機能 ---
class ProfileEditView(LoginRequiredMixin, generic.UpdateView):
    model = UserProfile
    fields = ['avatar', 'bio']
    template_name = 'gallery/profile_edit.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        obj, created = UserProfile.objects.get_or_create(user=self.request.user)
        return obj

# --- 6. 削除機能（単体） ---
class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ArtPost
    template_name = 'gallery/post_confirm_delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# --- 7. 一括削除機能 ---
@require_POST
def bulk_delete(request):
    ids = request.POST.getlist('delete_ids')
    if ids and request.user.is_authenticated:
        ArtPost.objects.filter(id__in=ids, author=request.user).delete()
    return redirect('index')