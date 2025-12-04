from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 管理画面
    path('admin/', admin.site.urls),
    
    # アプリ（gallery）のURL
    path('', include('gallery.urls')),
    
    # ログイン機能（accounts/login/など）
    path('accounts/', include('django.contrib.auth.urls')),
]

# ▼ 画像を表示するための重要な設定！
# （これがないと、アップロードした画像が「404 Not Found」になります）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)