from django.contrib.auth.models import User


class UserFactory:
    def __init__(self, username='username', email='email@gmail.com',
                 password='password'):
        self.username = username
        self.email = email
        self.password = password

    def make_user(self):
        return(User.objects.create_user(
            username='username',
            email='email@gmail.com',
            password='password'
        ))
