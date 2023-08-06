from __future__ import annotations
from enum import Enum
from typing import List, Optional, Any


class ScriptConstant:
    def __init__(
            self,
            datatype: DataType,
            name: str,
            value: Any
    ):
        self.datatype: DataType = DataType(datatype)
        self.name: str = name
        self.value: Any = value

        if self.datatype == DataType.INT and not isinstance(value, int):
            raise ValueError("Script constant value argument does not match given datatype.")
        elif self.datatype == DataType.FLOAT and not isinstance(value, float):
            raise ValueError("Script constant value argument does not match given datatype.")
        elif self.datatype == DataType.STRING and not isinstance(value, str):
            raise ValueError("Script constant value argument does not match given datatype.")

    def __repr__(
            self
    ):
        return 'ScriptConstant("{}", "{}", "{}")'.format(self.datatype, self.name, self.value)

    def __str__(
            self
    ):
        return "{} {} = {};".format(self.datatype, self.name, self.value)


class ScriptParam:
    def __init__(
            self,
            datatype: DataType,
            name: str,
            default: Optional[Any]
    ):
        self.datatype: DataType = DataType(datatype)
        self.name: str = name
        self.default: Optional[str] = default

    def __repr__(
            self
    ):
        return 'ScriptParam({}, {}, {})'.format(repr(self.datatype), repr(self.name), repr(self.default))

    def __str__(
            self
    ):
        if self.default is not None:
            return "{} {} = {}".format(self.datatype, self.name, self.default)
        else:
            return "{} {}".format(self.datatype, self.name)


class ScriptFunction:
    def __init__(
            self,
            returntype: DataType,
            name: str,
            params: List[ScriptParam],
            description: str,
            raw: str
    ):
        self.returntype: DataType = DataType(returntype)
        self.name: str = name
        self.params: List[ScriptParam] = params
        self.description: str = description
        self.raw: str = raw

    def __repr__(
            self
    ):
        return "ScriptFunction({}, {}, {}, {}, {})".format(repr(self.returntype), repr(self.name), repr(self.params),
                                                           repr(self.description), repr(self.raw))

    def __str__(
            self
    ):
        param_str = ""
        for param in self.params:
            param_str += str(param)
            if param is not self.params[-1]:
                param_str += ", "
        return "{} {}({})".format(self.returntype, self.name, param_str)


class DataType(Enum):
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    STRING = "string"
    OBJECT = "object"
    VECTOR = "vector"
    LOCATION = "location"
    EVENT = "event"
    EFFECT = "effect"
    ITEMPROPERTY = "itemproperty"
    TALENT = "talent"
    ACTION = "action"
    STRUCT = "struct"

    def size(self) -> int:
        if self == DataType.VOID:
            return 0
        elif self == DataType.VECTOR:
            return 12
        elif self == DataType.STRUCT:
            raise ValueError  # TODO
        else:
            return 4
