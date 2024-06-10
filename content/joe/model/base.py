"""File housing exclusively the base JourneyObject
"""
# ======== standard imports ========
from dataclasses import dataclass, fields, asdict, Field, is_dataclass
from datetime import datetime
from enum import Enum, EnumMeta
from typing import Type, Any, Union, Iterable, Optional, get_origin, get_args
from types import GenericAlias, UnionType, NoneType
import json
from json import JSONEncoder
from json import JSONDecoder
import warnings
from itertools import product
# ==================================

# ======= third party imports ======
# ==================================

# ========= program imports ========
# ==================================


def product_dict(**kwargs):
    keys = kwargs.keys()
    return [dict(zip(keys, instance)) for instance in product(*kwargs.values())]


def add_one_tab(tabbed_str: str):
    new_tabbed_str = tabbed_str.split('\n')
    new_tabbed_str = ['\t' + newline for newline in new_tabbed_str]
    return '\n'.join(new_tabbed_str)


@dataclass
class JourneyObject:
    ''' A base data schema for Journey data objects '''
    id: str
    creation_date: datetime
    update_date: datetime

    attribute_doc_strings = None
    example = None

    def str_helper(self, depth):
        basestr = [(depth * '\t') + 'Python Obj ID: ' + hex(id(self))]
        nested_str = []
        for field in fields(self):
            if is_dataclass(field.type):
                nested_str.append(
                    (depth*'\t') + field.name + ':\n'
                    + add_one_tab(str(getattr(self, field.name)))
                )
            elif get_origin(field.type) is list:
                clist = getattr(self, field.name)
                #if isinstance(clist[0], )
                nested_str.append(
                    (depth*'\t') + field.name + ': [\n' 
                    + ('\n' + ((depth*'\t'))).join([add_one_tab(str(ele)) for ele in clist])
                    + '\n' + (depth*'\t') + ']'
                )
            else:
                basestr.append((depth*'\t') + field.name +': ' +str(getattr(self, field.name)))
        all_str = basestr
        all_str += nested_str
        all_str = [(depth*'\t') + str(self.__class__)] + all_str
        return '\n'.join(all_str)

    def __str__(self):
        return self.str_helper(depth=0)

    def validate(self):
        [getattr(self, method_name)() for method_name in dir(self)
         if method_name.startswith('validate_') and callable(getattr(self, method_name))]
        
    def _warncast(self, varname:str, var, intype:type, outtype:type):
        warnings.warn(f'Casting {varname} from {intype} to {outtype}.')
        return outtype(var)

    def _deserialize_str(self, field:Field, inbound_var):
        if field.type is datetime:
            setattr(self, field.name, datetime.fromisoformat(inbound_var))
        elif isinstance(field.type, EnumMeta) and inbound_var in field.type._value2member_map_:
            setattr(self, field.name, field.type._value2member_map_[inbound_var])
        else:
            pass

    @staticmethod
    def is_optional(field_type) -> bool:
        return (get_origin(field_type) is Union or get_origin(field_type) is UnionType) and type(None) in get_args(field_type)

    @staticmethod
    def decompose_type(obj_type) -> tuple[Optional[Type], Optional[tuple]]:
        origin = get_origin(obj_type)
        if origin is list:
            return list, get_args(obj_type)
        elif origin is tuple: 
            return tuple, get_args(obj_type)
        elif origin is dict:
            key_args, value_args = get_args(obj_type)
            # We know the keys can really only take Unions due to hashablity
            key_args = key_args
            value_args = value_args
            return (
                dict,
                (
                    key_args, 
                    value_args
                )
            )
        elif (origin is Union or origin is UnionType):
            return (
                None, 
                get_args(obj_type)
            )
        else:
            if obj_type is list:
                return list, tuple()
            elif obj_type is tuple:
                return tuple, tuple()
            elif obj_type is dict:
                return dict, tuple()
            else:
                return None, (obj_type,)

    def deserialize_simple_var(self, varname, inbound_var, expected_types):
        error_str = 'While trying to construct '+ str(self.__class__)+ ', a field failed to be parsed.'\
            '\n\tVariable Name: {}\n\tInbound Variable: {}\n\tExpected Types: {}'
        uniform_typed = len(expected_types) == 1
        # ========== Primitive Types ===========
        if inbound_var is None and NoneType in expected_types:
            return inbound_var
        match inbound_var:
            case bool() if bool in expected_types: # Make sure to put this before int
                return inbound_var
            case int() if int in expected_types:
                return inbound_var
            case int() if not int in expected_types:
                if uniform_typed and float is expected_types[0]:
                    return self._warncast(varname, inbound_var, int, float)
                elif uniform_typed and bool is expected_types[0]:
                    return self._warncast(varname, inbound_var, int, bool)
                else:
                    raise self.JourneyUserInputException(varname, error_str.format(varname, inbound_var.__repr__(), expected_types))
            case float() if float in expected_types:
                return inbound_var
            case float() if not float in expected_types:
                if uniform_typed and int is expected_types[0]:
                    return self._warncast(varname, float, int)
                else:
                    raise self.JourneyUserInputException(varname, error_str.format(varname, inbound_var.__repr__(), expected_types))
            case str() if str in expected_types:
                return inbound_var
            case list() if list in expected_types:
                return inbound_var
            case dict() if dict in expected_types:
                return inbound_var
        # ========== Serialized Types ==========
            case str() if not str in expected_types:
                if uniform_typed and datetime is expected_types[0]:
                    return datetime.fromisoformat(inbound_var)
                elif uniform_typed and isinstance(expected_types[0], EnumMeta):
                    if inbound_var in expected_types[0]._value2member_map_:
                        return expected_types[0]._value2member_map_[inbound_var]
                    else:
                        raise self.JourneyUserInputException(
                            varname, 
                            (
                                error_str.format(varname, inbound_var, expected_types)
                                + '\n\tNotably, it appears the string provided is not a member of the Enum targeted.'
                            )
                        )
                else:  # Serialized string is assumed unique ID of JOE Object
                    return inbound_var
            case dict():
                for i in range(len(expected_types)):
                    if expected_types[i] in JourneyObject.__subclasses__():
                        return expected_types[i](**inbound_var)
                raise self.JourneyUserInputException(
                    varname, (
                        'DICT:\n'
                        +error_str.format(varname, inbound_var.__repr__(), expected_types)
                    )
                )
        # ========= Deserialized Types =========
            case JourneyObject():
                return inbound_var
            case datetime() if datetime in expected_types:
                return inbound_var
            case EnumMeta():
                return inbound_var
            case _:
                # We got either a new or complicated type
                caught_type_exception_pairs = []
                for expected_type in expected_types:
                    exterior_data_structure, interior_expected_types = JourneyObject.decompose_type(expected_type)
                    try:
                        if exterior_data_structure is None and len(interior_expected_types) == 1:
                            if isinstance(inbound_var, interior_expected_types):
                                return inbound_var
                            else:
                                raise self.JourneyUserInputException(varname, error_str.format(varname, inbound_var.__repr__(), expected_types))
                        else:
                            parsed_var = self.deserialize_var(varname, inbound_var, exterior_data_structure, interior_expected_types)
                            return parsed_var
                    except Exception as e:
                        caught_type_exception_pairs.append((expected_type, e))
                raise self.JourneyUserInputException(
                    varname, 
                    (
                        'FINAL:\n'+error_str.format(varname, inbound_var.__repr__(), expected_types)
                        + '\nTried all the expected types, and got the following exceptions:\n'
                        + '\n'.join([f'Expected Type:\n\t{et}\nCaught Exception:\n\t{ex}' for et, ex in caught_type_exception_pairs])
                    )
                )
    
    def deserialize_var(self, varname, inbound_var, exterior_data_structure, interior_expected_types):
        if exterior_data_structure is None: # If the expected type is a Primitive or Object
            return self.deserialize_simple_var(varname, inbound_var, interior_expected_types)
        elif exterior_data_structure is list and isinstance(inbound_var, list):
            if len(interior_expected_types) == 0:
                return inbound_var
            else:
                return [
                    self.deserialize_simple_var(varname+'_'+str(i), inbound_ele, interior_expected_types)
                    for i, inbound_ele in enumerate(inbound_var)
                ]
        elif exterior_data_structure is tuple and isinstance(inbound_var, (tuple, list)):
            if len(interior_expected_types) == 0:
                return tuple(inbound_var)
            elif len(interior_expected_types) == 1: # Assume they want this type for the whole tuple
                return tuple([
                    self.deserialize_simple_var(varname+'_'+str(i), inbound_ele, (interior_expected_types[0],))
                    for i, inbound_ele in enumerate(inbound_var)
                ])
            elif len(interior_expected_types) > 1 and len(interior_expected_types) == len(inbound_var):
                return tuple([
                    self.deserialize_simple_var(varname+'_'+str(i), inbound_ele, (interior_expected_types[i],))
                    for i, inbound_ele in enumerate(inbound_var)
                ])
            else:
                raise self.JourneyUserInputException(
                    varname, 
                    f'The length of the inbound variable does not match the number of types provided.\n{inbound_var}\n{interior_expected_types}'
                )
        elif exterior_data_structure is dict and isinstance(inbound_var, dict):
            if len(interior_expected_types) == 0:
                return inbound_var
            else:
                return {
                    self.deserialize_simple_var(varname+'_key_'+str(key), key, interior_expected_types[0]):
                    self.deserialize_var(value+'_value_'+str(value), value, interior_expected_types[1])
                    for key, value in inbound_var.items()
                }
        elif exterior_data_structure is dict and not isinstance(inbound_var, dict):
            raise self.JourneyUserInputException(varname, f'Expected a dict but got {inbound_var}')
        elif exterior_data_structure is list and not isinstance(inbound_var, list):
            raise self.JourneyUserInputException(varname, f'Expected a list but got {inbound_var}')
        elif exterior_data_structure is tuple and not isinstance(inbound_var, (tuple, list)):
            raise self.JourneyUserInputException(varname, f'Expected a tuple but got {inbound_var}')
        else:
            raise self.JourneyUserInputException(varname, f'Could not identify field data structure')



    def __post_init__(self):
        for field in fields(self):
            inbound_var = getattr(self, field.name)
            exterior_data_structure, interior_expected_types = JourneyObject.decompose_type(field.type)
            setattr(self, field.name, self.deserialize_var(field.name, inbound_var, exterior_data_structure, interior_expected_types))
            

        # Secondary Check
        for field in fields(self):
            exterior_expected_type, interior_expected_types = JourneyObject.decompose_type(field.type)
            accepted_value = getattr(self, field.name)
            try:
                if exterior_expected_type is None:
                    pass
                    #self.check_type(field.name, accepted_value, interior_expected_types)
                else:
                    pass
                    #self.check_type(field.name, accepted_value, exterior_expected_type)
                    if len(interior_expected_types) > 0:
                        if exterior_expected_type is list:
                            pass
                        elif exterior_expected_type is tuple:
                            pass
                        elif exterior_expected_type is dict:
                            pass
                            #self.check_iterable_typing(field.name, accepted_value.keys(), interior_expected_types[0])
                            #self.check_iterable_typing(field.name, accepted_value.values(), interior_expected_types[1])
            except Exception:
                print(f"Failed {field.name} on {self}")
                print(exterior_expected_type, interior_expected_types)
                raise

        # Consolidate same variables
        self.consolidate_family_tree()

        self.validate()

    @staticmethod
    def strip_typing(column_type) -> tuple[Type, dict[str, Any]]:
        column_kwargs = {}

        # Handle optional arguments
        if JourneyObject.is_optional(column_type):
            arg_types = get_args(column_type)
            arg_types = [arg_type for arg_type in arg_types if not arg_type is type(None)]
            if len(arg_types) > 1:
                raise TypeError(f"Unrecognized column type: {column_type}")
            else:
                column_type = arg_types[0]
                column_kwargs.update({'nullable': True})

        # Attend to generics
        origin_column_type = get_origin(column_type)
        column_type = column_type if origin_column_type is None else origin_column_type
        return column_type, column_kwargs

    class JourneyException(Exception):
        pass

    class JourneyUserInputException(JourneyException):
        def __init__(self, parameter_name: str, message: str = '') -> None:
            super().__init__(
                f'Invalid argument provided for {parameter_name}.'
                + ' ' + message
            )

    class JUITypeError(JourneyUserInputException):
        def __init__(self, parameter_name: str, expected_type: str, given_arg: Any):
            message = f'Expected {parameter_name} to have type {expected_type}, but recieved\n{given_arg}\n with type {type(given_arg)}.'
            super().__init__(parameter_name, message=message)

    class JUIFixedLengthError(JourneyUserInputException):
        def __init__(self, parameter_name: str, expected_length: int, given_arg: Iterable):
            message = f'Expected {parameter_name} to have length {expected_length}, but recieved\n{given_arg}\n with length {len(given_arg)}.'
            super().__init__(parameter_name, message=message)

    class JUIChoiceError(JourneyUserInputException):
        def __init__(self, parameter_name: str, permissable_choices: Iterable, given_arg: Any) -> None:
            message = f'Expected {parameter_name} to be one of {permissable_choices}, but recieved\n{given_arg}.'
            super().__init__(parameter_name, message=message)

    class JUIBoundsError(JourneyUserInputException):
        def __init__(self, parameter_name: str, min_bound: int | float, max_bound: int | float, given_arg: Any) -> None:
            message = f'Expected {parameter_name} to be within ({min_bound}, {max_bound}), but recieved\n{given_arg}.'
            super().__init__(parameter_name, message=message)

    class JUISelectionError(JourneyUserInputException):
        def __init__(self, constructor_classname, *parameter_names):
            message = f'One of {parameter_names} must be provided to construct {constructor_classname}.'
            super().__init__(', '.join(parameter_names), message=message)

    class JUIXORError(JourneyUserInputException):
        def __init__(self, constructor_classname, *parameter_names):
            message = f'If one of {parameter_names} is provided, all of {parameter_names} must be provided to construct {constructor_classname}.'
            super().__init__(', '.join(parameter_names), message=message)

    @classmethod
    def check_type(cls, arg_name: str, arg: Any, desired_type: Any):
        #try:
        if not isinstance(arg, desired_type):
            raise cls.JUITypeError(arg_name, desired_type, arg)
        #except Exception as e:
            #print(f"Failed type check: {e}, with arg_name: {arg_name}, desired_type: {desired_type}")

    @classmethod
    def check_iterable_typing(cls, arg_name: str, arg: Any, desired_inner_type: Any, fixed_length: Optional[int] = None):
        cls.check_type(arg_name, arg, Iterable)
        if fixed_length is not None and len(arg) != fixed_length:
            raise cls.JUIFixedLengthError(arg_name, fixed_length, arg)
        for i, ele in enumerate(arg):
            cls.check_type(arg_name + f'[{i}]', desired_inner_type, ele)
            #if not isinstance(ele, desired_inner_type):
            #    raise cls.JUITypeError(arg_name + f'[{i}]', desired_inner_type, ele)

    @classmethod
    def check_choice_validity(cls, arg_name: str, arg: Any, permissable_choices: Iterable):
        if not (arg in permissable_choices):
            raise cls.JUIChoiceError(arg_name, permissable_choices, arg)

    @classmethod
    def check_bound(cls, arg_name: str, arg: Any,
                    min_bound: None | int | float = None,
                    max_bound: None | int | float = None):
        if (min_bound is not None and min_bound > arg) or \
           (max_bound is not None and max_bound < arg):
            raise cls.JUIBoundsError(arg_name, min_bound, max_bound, arg)

    @classmethod
    def from_json(cls, object_str: str):
        return cls(**json.loads(object_str))

    @classmethod
    def JourneyObjectFieldSerializer(cls, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, dict):
            return json.dumps({
                key: cls.JourneyObjectFieldSerializer(value)
                for key, value in obj.items()})
        elif isinstance(obj, list):
            return json.dumps([cls.JourneyObjectFieldSerializer(obj_item)
                for obj_item in obj])
        elif isinstance(type(obj), EnumMeta):
            return obj.value
        elif isinstance(obj, JourneyObject):
            return obj.id
        return obj

    def to_json(self):
        return json.dumps({
            field.name: self.JourneyObjectFieldSerializer(getattr(self, field.name))
            for field in fields(self)})
    
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.to_json() == other.to_json()

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def joe_children(self) -> dict[str, 'JourneyObject']:
        descendents = {}
        for field in fields(self):
            if field.type in JourneyObject.__subclasses__():
                descendents[field.name] = getattr(self, field.name)
        return descendents
    
    def consolidate_family_tree(self, all_joe_objs = []):
        all_direct_children = self.joe_children()

        for joe_name, current_child in all_direct_children.items():
            if not isinstance(current_child, str):
                setattr(self, joe_name, current_child.consolidate_family_tree(all_joe_objs))

        for existing_obj in all_joe_objs:
            if self == existing_obj:
                return existing_obj
            
        all_joe_objs.append(self)
        return self
    
    @classmethod
    def get_serialized_tests(cls) -> list[dict]:
        input_vals = {}
        for field in fields(cls):
            expected_type = field.type
            input_vals[field.name] = []

            if cls.is_optional(expected_type):
                input_vals[field.name].append(None)
                expected_type = [type_arg for type_arg in get_args(expected_type) if type_arg is not NoneType][0]
            if expected_type in (bool, int, float, list, dict):
                input_vals[field.name].append(cls.example[field.name])
            elif expected_type in JourneyObject.__subclasses__():
                input_vals[field.name].append(cls.example[field.name])
            elif isinstance(expected_type, EnumMeta):
                input_vals[field.name]+= [enum_value for enum_value in expected_type._value2member_map_.keys()]
            elif expected_type is datetime:
                input_vals[field.name].append(cls.example[field.name])
            else:
                input_vals[field.name].append(cls.example[field.name])

        return product_dict(**input_vals)
    
    @classmethod
    def get_deserialized_tests(cls) -> list[dict]:
        input_vals = {}
        for field in fields(cls):
            expected_type = field.type
            input_vals[field.name] = []

            if cls.is_optional(expected_type):
                input_vals[field.name].append(None)
                expected_type = [type_arg for type_arg in get_args(expected_type) if type_arg is not NoneType][0]

            if expected_type in (bool, int, float, list, dict):
                input_vals[field.name].append(cls.example[field.name])
            elif expected_type in JourneyObject.__subclasses__():
                input_vals[field.name].append(expected_type(**cls.example[field.name]))
            elif isinstance(expected_type, EnumMeta):
                input_vals[field.name]+= [enum_var for enum_var in expected_type._value2member_map_.values()]
            elif expected_type is datetime:
                input_vals[field.name].append(cls.example[field.name])
            else:
                input_vals[field.name].append(cls.example[field.name])

        return product_dict(**input_vals)
        
