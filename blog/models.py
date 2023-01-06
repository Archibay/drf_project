from django.db import models
from django.utils import timezone
from django_lifecycle import LifecycleModel, hook, AFTER_UPDATE
from django.urls import reverse
from django.conf import settings
from .tasks import send_mail as celery_send_mail
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Post(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published = models.BooleanField(default=False)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='post', on_delete=models.CASCADE)
    # highlighted = models.TextField()

    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = 'table' if self.linenos else False
    #     options = {'title': self.title} if self.title else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                               full=True, **options)
    #     self.highlighted = highlight(self.text, lexer, formatter)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comments(LifecycleModel):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    owner = models.ForeignKey('auth.User', related_name='comments', on_delete=models.CASCADE)
    # highlighted = models.TextField()

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

    # def save(self, *args, **kwargs):
    #     """
    #     Use the `pygments` library to create a highlighted HTML
    #     representation of the code snippet.
    #     """
    #     lexer = get_lexer_by_name(self.language)
    #     linenos = 'table' if self.linenos else False
    #     options = {'title': self.text} if self.text else {}
    #     formatter = HtmlFormatter(style=self.style, linenos=linenos,
    #                               full=True, **options)
    #     self.highlighted = highlight(self.text, lexer, formatter)
    #     super().save(*args, **kwargs)

    def __str__(self):
        return self.text
