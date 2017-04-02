from unittest import TestCase
from db import SQLUtil


class TestSQLUtil(TestCase):
    def test_new_user(self):
        util = SQLUtil('xtrix_test.db')
        # util.reset()
        # self.fail()
        self.assertEquals(util.new_user(1, 'me', user_rights=-1, user_rating=-1),
                          util.get_user(1))

    def test_get_user(self):
        self.fail()
