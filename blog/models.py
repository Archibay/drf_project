from django.db import models
from django.utils import timezone
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE
from django.urls import reverse
from django.conf import settings
from .tasks import send_mail as celery_send_mail


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Comments(LifecycleModel):
    username = models.CharField(max_length=200)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    @hook(AFTER_UPDATE, when='published', was=False, is_now=True)
    def owner_inform(self):
        post_id = self.post.id
        mail_to = self.post.user.email
        get_url = reverse('blog:post_detail', args=[post_id])
        subject = 'New comment'
        message = f'New comment was added - {settings.SCHEMA}://{settings.DOMAIN}:{settings.PORT}{get_url}'
        from_email = 'no_reply@somecompany.com'
        to_email = [mail_to]
        celery_send_mail.delay(subject, message, from_email, to_email)

    def __str__(self):
        return self.text
