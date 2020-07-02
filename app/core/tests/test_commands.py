from unittest.mock import patch

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandsTestCase(TestCase):

    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""

        # 実際にDBに接続するところの処理をMockのpatchを用いて置き換える
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # mockの返り値を定義
            gi.return_value = True
            # call_command(): 指定したコマンドを実行する
            call_command('wait_for_db')
            # mockの箇所が呼ばれた回数が1回であることを確認
            self.assertEqual(gi.call_count, 1)

    # DB接続に失敗したと仮定した際のtime.sleepをmockで置き換え省略する
    @patch('time.sleep', return_value=None)
    def test_wait_for_db(self, ts): #引数にデコレータで作成したmockを渡すことを忘れない
        """Test waiting for db"""

        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # side_effect: 例外を発生させたり、動的に返り値を変えたい場合に使う
            gi.side_effect = [OperationalError] * 5 + [True]
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
