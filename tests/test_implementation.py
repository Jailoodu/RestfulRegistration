import unittest
from unittest import mock
from api.implementation import *
from tests.test_utils import User_Object, convert_to_dict

class Get_List_Test(unittest.TestCase):
    @mock.patch('api.implementation.get_collection')
    def test_func(self, get_func):
        expected_collection = [User_Object("Tom", "vvppun", "Confirmed", 22), User_Object("Jay", "1xx8eN", "Accepted", 19), User_Object("Sarah", "9TVVXM", "Confirmed", 25), User_Object("Darcy", "YYnWnS", "Confirmed", 23)]
        get_func.return_value = expected_collection

        expected_dict = convert_to_dict(expected_collection)
        output = get_users_list()

        # assertions
        self.assertCountEqual(output, expected_dict)
        get_func.assert_called_once()

class Get_Empty_List_Test(unittest.TestCase):
    @mock.patch('api.implementation.get_collection')
    def test_func(self, get_func):
        expected_collection = []
        get_func.return_value = expected_collection

        expected_dict = convert_to_dict(expected_collection)
        output = get_users_list()

        # assertions
        self.assertCountEqual(output, expected_dict)
        get_func.assert_called_once()

class Get_User_Test(unittest.TestCase):
    @mock.patch('api.implementation.get_object')
    def test_func(self, get_func):
        expected = [User_Object("Tom", "YYnWnS", "Confirmed", 22)]
        get_func.return_value = expected

        user_detail = get_user("YYnWnS")
        self.assertCountEqual([user_detail], convert_to_dict(expected))
        get_func.assert_called_once()

class Get_Null_User_Test(unittest.TestCase):
    @mock.patch('api.implementation.get_object')
    def test_func(self, get_func):
        expected = []
        get_func.return_value = expected

        user_detail = get_user("YYnWnS")
        self.assertIsNone(user_detail)
        get_func.assert_called_once()

class Get_User_ID_Test(unittest.TestCase):
    @mock.patch('api.implementation.fetch_firestore_id')
    def test_func(self, get_func):
        expected = [User_Object("Tom", "YYnWnS", "Confirmed", 22)]
        get_func.return_value = expected

        id = get_firestore_id(expected[0].get_id())
        self.assertEqual(id, expected[0].get_id())
        get_func.assert_called_once()

class Get_Null_User_ID_Test(unittest.TestCase):
    @mock.patch('api.implementation.fetch_firestore_id')
    def test_func(self, get_func):
        expected = None
        get_func.return_value = expected

        non_existent_id = "1234567890abc"
        id = get_firestore_id(non_existent_id)
        self.assertIsNone(id)
        get_func.assert_called_once()

class Get_User_Payment_Details_Test(unittest.TestCase):
    @mock.patch('api.implementation.get_payment_details')
    def test_func(self, get_func):
        user = User_Object("Jane", "87HV2NN", "Pending", 24)
        expected_return = {"status": "Pending", "amount":45.99}
        get_func.return_value = expected_return

        data = get_payment_details(user.get_id())
        self.assertEqual(data, expected_return)
        get_func.assert_called_once()

class Get_Null_User_Payment_Details_Test(unittest.TestCase):
    @mock.patch('api.implementation.get_payment_details')
    def test_func(self, get_func):
        non_existent_id = "78hjg4v2nb44k"
        expected_return = {}
        get_func.return_value = expected_return

        data = get_payment_details(non_existent_id)
        self.assertEqual(data, expected_return)
        get_func.assert_called_once()

class Make_Payment_Test(unittest.TestCase):
    @mock.patch('api.implementation.make_payment')
    def test_func(self, get_func):
        payload = {"status": "Confirmed", "id":"76rfg43gf3gh9"}

        make_payment(payload)
        get_func.assert_called_once() 

class Make_Empty_Payment_Test(unittest.TestCase):
    @mock.patch('api.implementation.make_payment')
    def test_func(self, get_func):
        payload = {}

        make_payment(payload)
        get_func.assert_called_once() 