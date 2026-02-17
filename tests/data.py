import random
import string

from surety.sdk.array import Array, Set
from surety.sdk.dictionary import Dictionary
from surety.sdk.field import Field


class TypeOne(Field):
    def generate_value(self):
        return ''.join(random.sample(string.ascii_letters + string.digits, 6))


class TypeTwo(Field):
    def generate_value(self):
        return random.randint(0, 1000)


class Base(Dictionary):
    StringField = TypeOne(name='string_field')
    IntField = TypeTwo(name='int_field')


class Optional(Dictionary):
    OptString = TypeOne(name='opt_string', required=False)
    OptInt = TypeTwo(name='opt_int', required=False)


class AllowedNone(Dictionary):
    NoneString = TypeOne(name='none_str', allow_none=True)
    NoneInt = TypeTwo(name='none_int', allow_none=True)
    OptNoneInt = TypeTwo(name='opt_none_int', allow_none=True,
                         required=False)


class ComposeBase(Dictionary):
    FirstBase = Base(name='first_base')
    SecondBase = Base(name='second_base')
    ThirdBase = Base(name='third_base')
    OptBase = Base(name='opt_base', required=False)


class ComposeOptional(Dictionary):
    FirstOpt = Optional(name='first_optional')
    OptionalOpt = Optional(name='optional_opt', required=False)


class Mix(Dictionary):
    ReqBase = Base(name='req_base')
    OptBase = Base(name='opt_base', required=False)
    NotNoneAllowedNone = AllowedNone(name='not_allowed')
    NoneAllowedNone = AllowedNone(name='none_allowed', allow_none=True)
    ReqOptional = Optional(name='req_optional')
    OptOptional = Optional(name='opt_optional', required=False)
    ReqTypeArray = Array(TypeOne, name='req_type_array')
    ReqTypeSet = Set(TypeOne, name='req_type_set')
    OptTypeArray = Array(TypeOne, name='opt_type_array', required=False)
    OptTypeSet = Set(TypeOne, name='opt_base_set', required=False)
    NoneTypeArray = Array(AllowedNone, name='none_type_array', allow_none=True)
    ReqBaseArray = Array(Base, name='req_base_array')
    OptBaseArray = Array(Base, name='opt_base_array', required=False)
    ReqFullBaseArray = Array(
        Base(is_full=True), name='req_full_base_array'
    )
    OptFullBaseArray = Array(
        Base(is_full=True), name='opt_full_base_array', required=False
    )
