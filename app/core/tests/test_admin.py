from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        # Client: 仮想的にWebブラウザからアクセスした振る舞いでテストが可能
        self.client = Client()

        # get_user_model(): 現時点で有効になっているUserモデル自体を呼び出す
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@gmail.com',
            password='password123'
        )

        # force_login(): login()よりも簡易的にログイン状態をシミュレートする
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@gmail.com',
            password='test12434',
            name='Test user full name'
        )

    def test_user_listed(self):
        """Test that users are listed on user page"""
        # 管理画面には以下のようにreverseで変換可能な「URL name」が用意されている
        # admin:{{ app_label }}_{{ model_name }}_changelist
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # assertContains(a,b): aの中にbが含まれるか
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # Sample URL: /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        # HTTPのgetメソッドを仮想的に実行
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
