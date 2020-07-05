import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):  # handle: commandが呼ぼれたときに実行する処理
        # メッセージを出力
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                # connections: DB接続が可能か確認
                db_conn = connections['default']
            except OperationalError:  # DBに接続できない時、DjangoはOperationalErrorを返す
                self.stdout.write('Database unavailable, waiting 1 second...')
                # 1秒間処理を停止
                time.sleep(1)

        # DBが利用可能と確認できたら、その旨を出力
        self.stdout.write(self.style.SUCCESS('Database available'))
