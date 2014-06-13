# encoding: utf-8

"""
Test suite for pptx.oxml.simpletypes module, which contains simple type class
definitions. A simple type in this context corresponds to an
``<xsd:simpleType>`` definition in the XML schema and provides data
validation and type conversion services for use by xmlchemy.
"""

from __future__ import absolute_import, print_function

import pytest

from pptx.oxml.simpletypes import BaseIntType, BaseSimpleType

from ..unitutil import method_mock, instance_mock


class DescribeBaseSimpleType(object):

    def it_can_convert_attr_value_to_python_type(self, from_xml_fixture):
        SimpleType, str_value_, py_value_ = from_xml_fixture
        py_value = SimpleType.from_xml(str_value_)
        SimpleType.convert_from_xml.assert_called_once_with(str_value_)
        assert py_value is py_value_

    def it_can_convert_python_value_to_string(self, to_xml_fixture):
        SimpleType, py_value_, str_value_ = to_xml_fixture
        str_value = SimpleType.to_xml(py_value_)
        SimpleType.validate.assert_called_once_with(py_value_)
        SimpleType.convert_to_xml.assert_called_once_with(py_value_)
        assert str_value is str_value_

    def it_can_validate_a_value_as_a_python_int(self, valid_int_fixture):
        value, expected_exception = valid_int_fixture
        if expected_exception is None:
            BaseSimpleType.validate_int(value)
        else:
            with pytest.raises(expected_exception):
                BaseSimpleType.validate_int(value)

    def it_can_validate_a_value_as_a_python_string(self, valid_str_fixture):
        value, expected_exception = valid_str_fixture
        if expected_exception is None:
            BaseSimpleType.validate_string(value)
        else:
            with pytest.raises(expected_exception):
                BaseSimpleType.validate_string(value)

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def from_xml_fixture(
            self, request, str_value_, py_value_, convert_from_xml_):
        return ST_SimpleType, str_value_, py_value_

    @pytest.fixture
    def to_xml_fixture(
            self, request, py_value_, str_value_, convert_to_xml_,
            validate_):
        return ST_SimpleType, py_value_, str_value_

    @pytest.fixture(params=[
        (42,    None),
        (0,     None),
        (-42,   None),
        ('42',  TypeError),
        (None,  TypeError),
        (42.42, TypeError),
    ])
    def valid_int_fixture(self, request):
        value, expected_exception = request.param
        return value, expected_exception

    @pytest.fixture(params=[
        ('foobar', None),
        ('',       None),
        (' foo ',  None),
        (('foo',), TypeError),
        (42,       TypeError),
        (None,     TypeError),
        (42.42,    TypeError),
    ])
    def valid_str_fixture(self, request):
        value, expected_exception = request.param
        return value, expected_exception

    # fixture components ---------------------------------------------

    @pytest.fixture
    def convert_from_xml_(self, request, py_value_):
        return method_mock(
            request, ST_SimpleType, 'convert_from_xml',
            return_value=py_value_
        )

    @pytest.fixture
    def convert_to_xml_(self, request, str_value_):
        return method_mock(
            request, ST_SimpleType, 'convert_to_xml',
            return_value=str_value_
        )

    @pytest.fixture
    def py_value_(self, request):
        return instance_mock(request, int)

    @pytest.fixture
    def str_value_(self, request):
        return instance_mock(request, str)

    @pytest.fixture
    def validate_(self, request):
        return method_mock(request, ST_SimpleType, 'validate')


class DescribeBaseIntType(object):

    def it_can_convert_a_string_to_an_int(self, from_xml_fixture):
        str_value, expected_value, expected_exception = from_xml_fixture
        if expected_exception is None:
            value = BaseIntType.convert_from_xml(str_value)
            assert value == expected_value
        else:
            with pytest.raises(expected_exception):
                BaseIntType.convert_from_xml(str_value)

    def it_can_convert_an_int_to_a_string(self, to_xml_fixture):
        value, expected_str_value = to_xml_fixture
        str_value = BaseIntType.convert_to_xml(value)
        assert str_value == expected_str_value

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('42',      42, None),
        ('-42',    -42, None),
        ('-0042',  -42, None),
        ('',      None, ValueError),
        ('foo',   None, ValueError),
        ('42.42', None, ValueError),
        ('0x0a3', None, ValueError),
        (None,    None, TypeError),
    ])
    def from_xml_fixture(self, request):
        str_value, expected_value, expected_exception = request.param
        return str_value, expected_value, expected_exception

    @pytest.fixture(params=[
        (42,   '42'),
        (-42, '-42'),
        (0x2A, '42'),
    ])
    def to_xml_fixture(self, request):
        value, expected_str_value = request.param
        return value, expected_str_value


# --------------------------------------------------------------------
# static fixture
# --------------------------------------------------------------------

class ST_SimpleType(BaseSimpleType):

    @classmethod
    def convert_from_xml(cls, str_value):
        return 666

    @classmethod
    def convert_to_xml(cls, value):
        return '666'

    @classmethod
    def validate(cls, value):
        pass