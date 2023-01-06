from django.core.management.base import BaseCommand
from blog.models import Post, Comments
from django.contrib.auth.models import User
from faker import Faker
import random
from django.contrib.auth import hashers

fake = Faker()


class Command(BaseCommand):
    help = 'Fill db'

    def add_arguments(self, parser):
        parser.add_argument('total_u', type=int, choices=range(0, 101), help='Numbers of Users')
        parser.add_argument('total_p', type=int, choices=range(0, 101), help='Numbers of Posts')
        parser.add_argument('total_c', type=int, choices=range(0, 101), help='Numbers of Comments')

    def handle(self, **kwargs):
        # add Users
        total_u = kwargs['total_u']
        User.objects.bulk_create(
            [User(username=fake.word(), first_name=fake.first_name(), last_name=fake.last_name(), email=fake.email(),
             password=hashers.make_password(str(fake.password()))) for i in range(total_u)]
        )

        # add Posts
        total_p = kwargs['total_p']
        u_list1 = User.objects.values_list('id', flat=True)
        for i in range(total_p):
            random_u1 = random.choice(u_list1)
            objs = Post(title=fake.sentence(nb_words=random.randrange(1, 5)),
                        text=fake.text(max_nb_chars=1000),
                        published=random.choice([True, False]),
                        owner=User.objects.get(id=random_u1))
            objs.save()

        # add Comments
        total_c = kwargs['total_c']
        p_list = Post.objects.values_list('id', flat=True)
        u_list2 = User.objects.values_list('id', flat=True)
        for b in range(total_c):
            random_p = random.choice(p_list)
            random_u2 = random.choice(u_list2)
            objs = Comments(text=fake.text(max_nb_chars=100),
                            post=Post.objects.get(id=random_p),
                            published=random.choice([True, False]),
                            owner=User.objects.get(id=random_u2))
            objs.save()
