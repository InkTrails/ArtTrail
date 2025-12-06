from django.db import models
from django.contrib.auth.models import User

# イラストに関するデータ
class ArtPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE) #外部キー多対一、道連れ削除
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='posts/')
    is_practice = models.BooleanField(default=False, verbose_name="模写（練習用）") #摸写フラグ
    
    TAG_CHOICES = [
        ('hand', '手の練習'),
        ('face', '顔・表情'),
        ('pose', '全身・ポーズ'),
        ('copy', '完全模写'),
        ('other', 'その他'),
    ]
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# プロフィールに関するデータ
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #一対一,道連れ削除 
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    def __str__(self):
        return f'{self.user.username} Profile'