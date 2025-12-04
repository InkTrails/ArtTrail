from django.contrib import admin
from .models import ArtPost

# 管理画面でArtPostを扱えるように登録！
admin.site.register(ArtPost)