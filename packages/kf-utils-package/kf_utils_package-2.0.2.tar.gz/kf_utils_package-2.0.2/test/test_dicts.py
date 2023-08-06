import unittest

from kf_utils import dicts
from test.resources import test_messages


class TestDicts(unittest.TestCase):
    """
    Test dicts scripts and methods
    """

    clean_dict_method = 'dicts.clean_dict'
    merge_dicts_method = 'dicts.merge_dicts'

    test_dict: dict = {
        "str_value": 'value',
        "int_value": 1,
        "bool_value": True,
        "none_value": None
    }
    test_dict_keys: list[str] = list(test_dict.keys())

    # 1. Test dicts.clean_dict method
    def test_clean_dict_not_valid_param(self) -> None:
        """
        GIVEN a not valid dict param \n
        WHEN dicts.clean_dict method is called \n
        THEN an AttributeError exception is raised
        """
        not_valid_param = 'I''m a string, not a dict'

        self.assertRaises(AttributeError, dicts.clean_dict, not_valid_param)

    def test_clean_dict_return_type(self) -> None:
        """
        GIVEN a valid dict param \n
        WHEN dicts.clean_dict method is called \n
        THEN dicts.clean_dict returned value is not None \n
        AND dicts.clean_dict returned value type is dict
        """
        clean_dict = dicts.clean_dict(self.test_dict)

        self.assertIsNotNone(
            clean_dict,
            test_messages.METHOD_RETURNS_NONE.format(method=self.clean_dict_method)
        )
        self.assertIsInstance(
            clean_dict,
            dict,
            test_messages.METHOD_RETURNED_VALUE_IS_NOT.format(method=self.clean_dict_method, value='dict')
        )

    def test_clean_dict_remove_null_values(self) -> None:
        """
        GIVEN a valid dict param \n
        AND contains null value \n
        WHEN dicts.clean_dict method is called \n
        THEN dicts.clean_dict returned dict values does not contain null values \n
        AND dicts.clean_dict returned dict keys are not equal to origin dict keys
        """
        self.test_clean_dict_return_type()

        clean_dict = dicts.clean_dict(self.test_dict)
        clean_dict_keys = list(clean_dict.keys())
        clean_dict_values = list(clean_dict.values())

        self.assertNotIn(
            None,
            clean_dict_values,
            test_messages.METHOD_RETURNED_OBJECT_CONTAINS_VALUE.format(
                method=self.clean_dict_method,
                returns='dict',
                value='None'
            )
        )
        self.assertNotEqual(
            self.test_dict_keys,
            clean_dict_keys,
            test_messages.IS_EQUAL.format(
                first='Origin dict',
                second='dicts.clean_dict returned dict'
            )
        )

    def test_merge_dicts_without_duplicated_values(self) -> None:
        """
        GIVEN two dictionaries \n
        WHEN dicts.merge_dicts is executed \n
        AND they don't contain duplicated keys \n
        THEN the merged dict is not none \n
        AND the merged dict contains all the keys from the original dicts \n
        AND the merged dict contains all the values from the original dicts
        """
        dic1: dict = {'a': 1, 'b': 2}
        dic2: dict = {'c': 3, 'd': 4}
        merged_dict = dicts.merge_dicts(dic1, dic2)

        self.assertIsNotNone(
            merged_dict,
            test_messages.METHOD_RETURNS_NONE.format(
                method=self.merge_dicts_method
            )
        )
        self.assertGreater(
            len(merged_dict),
            0,
            'The merged dict does not contain any item'
        )
        self.assertEqual(
            len(merged_dict),
            len(dic1) + len(dic2),
            'The merged dict does not contain all the items from the original dicts'
        )

        merged_dict_items = list(merged_dict.items())
        origin_items = list(dic1.items()) + list(dic2.items())
        for item in origin_items:
            self.assertIn(
                item,
                merged_dict_items,
                test_messages.METHOD_RETURNED_OBJECT_NOT_CONTAINS_VALUE.format(
                    method=self.merge_dicts_method,
                    returns='dict',
                    value=item
                )
            )

    def test_merge_dicts_more_than_two_dicts_without_duplicated_values(self) -> None:
        """
        GIVEN more than two dictionaries \n
        WHEN dicts.merge_dicts is executed \n
        AND they don't contain duplicated keys \n
        THEN the merged dict is not none \n
        AND the merged dict contains all the keys from the original dicts \n
        AND the merged dict contains all the values from the original dicts
        """
        dic1: dict = {'a': 1, 'b': 2}
        dic2: dict = {'c': 3, 'd': 4}
        dic3: dict = {'e': 5, 'f': 6}
        dic4: dict = {'h': 7}
        dic5: dict = {'i': 8, 'j': 9, 'k': 10}
        merged_dict = dicts.merge_dicts(dic1, dic2, dic3, dic4, dic5)

        self.assertIsNotNone(
            merged_dict,
            test_messages.METHOD_RETURNS_NONE.format(
                method=self.merge_dicts_method
            )
        )
        self.assertGreater(
            len(merged_dict),
            0,
            'The merged dict does not contain any item'
        )
        self.assertEqual(
            len(merged_dict),
            len(dic1) + len(dic2) + len(dic3) + len(dic4) + len(dic5),
            'The merged dict does not contain all the items from the original dicts'
        )

        merged_dict_items = list(merged_dict.items())
        origin_items = list(dic1.items()) + list(dic2.items()) + list(dic3.items()) + list(dic4.items()) + list(
            dic5.items())
        for item in origin_items:
            self.assertIn(
                item,
                merged_dict_items,
                test_messages.METHOD_RETURNED_OBJECT_NOT_CONTAINS_VALUE.format(
                    method=self.merge_dicts_method,
                    returns='dict',
                    value=item
                )
            )

    def test_merge_dicts_with_duplicated_values(self) -> None:
        """
        GIVEN two dictionaries \n
        WHEN dicts.merge_dicts is executed \n
        AND they contain duplicated keys \n
        THEN the merged dict is not none \n
        AND the merged dict contains all the keys from the original dicts \n
        AND the merged dict contains all the values from the original dicts \n
        AND the merged dict does not contain duplicated values
        """
        dic1: dict = {'a': 1, 'b': 2}
        dic2: dict = {'b': 3, 'c': 4}
        merged_dict = dicts.merge_dicts(dic1, dic2)

        self.assertIsNotNone(
            merged_dict,
            test_messages.METHOD_RETURNS_NONE.format(
                method=self.merge_dicts_method
            )
        )
        self.assertGreater(
            len(merged_dict),
            0,
            'The merged dict does not contain any item'
        )
        self.assertGreater(
            len(merged_dict),
            0,
            'The merged dict does not contain any item'
        )
        self.assertNotEqual(
            len(merged_dict),
            len(dic1) + len(dic2),
            'The merged dict contains duplicated values'
        )

        merged_dict_keys = list(merged_dict.keys())
        original_dicts_keys = set(list(dic1.keys()) + list(dic2.keys()))
        for key in original_dicts_keys:
            self.assertIn(
                key,
                merged_dict_keys,
                test_messages.METHOD_RETURNED_OBJECT_NOT_CONTAINS_VALUE.format(
                    method=self.merge_dicts_method,
                    returns='dict',
                    value=key
                )
            )

    def test_merge_dicts_no_args(self) -> None:
        """
        GIVEN no args \n
        WHEN dicts.merge_dicts is executed \n
        THEN the merged dict is not none \n
        AND the merged dict is empty
        """
        empty_merged_dict = dicts.merge_dicts()

        self.assertIsNotNone(
            empty_merged_dict,
            test_messages.METHOD_RETURNS_NONE.format(
                method=self.merge_dicts_method
            )
        )
        self.assertEqual(
            len(empty_merged_dict),
            0,
            'The merged dict contains items. Should be empty.'
        )
