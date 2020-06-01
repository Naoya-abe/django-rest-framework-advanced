# testに関するclassを継承
from django.test import TestCase
# 現時点で有効になっているUserモデルを呼び出す
from django.contrib.auth import get_user_model


class ModelTest(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'tonpei@pigmail.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # check_password: passwordがあっているかの確認
        self.assertTrue(user.check_password(password))

        # 現在はデフォルトのUsermodelを使用しているため、以下のエラーが表示される
        # TypeError: create_user() missing 1 required positional argument: 'username'
