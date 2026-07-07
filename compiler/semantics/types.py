from enum import Enum, auto

class Type:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

class PrimitiveType(Type):
    pass

class CollectionType(Type):
    def __init__(self, name: str, element_types: list[Type]):
        super().__init__(name)
        self.element_types = element_types
        
    def __repr__(self):
        if self.element_types:
            inner = ", ".join(str(t) for t in self.element_types)
            return f"{self.name}<{inner}>"
        return self.name

class UserType(Type):
    pass

class ClassType(UserType):
    pass

class InterfaceType(UserType):
    pass

class FunctionType(Type):
    def __init__(self, param_types: list[Type], return_type: Type):
        super().__init__("Function")
        self.param_types = param_types
        self.return_type = return_type

    def __repr__(self):
        params = ", ".join(str(p) for p in self.param_types)
        return f"({params}) -> {self.return_type}"

class ModuleType(Type):
    pass

class ResultType(Type):
    def __init__(self, success_type: Type, error_type: Type):
        super().__init__("Result")
        self.success_type = success_type
        self.error_type = error_type

    def __repr__(self):
        return f"Result<{self.success_type}, {self.error_type}>"

class UnknownType(Type):
    def __init__(self):
        super().__init__("Unknown")

class TypeRegistry:
    def __init__(self):
        self.NUMBER = PrimitiveType("number")
        self.STRING = PrimitiveType("string")
        self.BOOL = PrimitiveType("bool")
        self.VOID = PrimitiveType("void")
        self.UNKNOWN = UnknownType()
        
        self._types: dict[str, Type] = {
            "number": self.NUMBER,
            "string": self.STRING,
            "bool": self.BOOL,
            "void": self.VOID,
            "unknown": self.UNKNOWN
        }

    def register(self, t: Type):
        self._types[t.name] = t
        
    def get(self, name: str) -> Type | None:
        return self._types.get(name)

    def get_list(self, element_type: Type) -> CollectionType:
        # Cache list types to maintain canonical identity
        name = f"list<{element_type.name}>"
        if name not in self._types:
            self._types[name] = CollectionType("list", [element_type])
        return self._types[name]

    def get_dict(self, key_type: Type, val_type: Type) -> CollectionType:
        name = f"dict<{key_type.name}, {val_type.name}>"
        if name not in self._types:
            self._types[name] = CollectionType("dict", [key_type, val_type])
        return self._types[name]
        
    def get_result(self, success_type: Type, error_type: Type) -> ResultType:
        name = f"Result<{success_type.name}, {error_type.name}>"
        if name not in self._types:
            self._types[name] = ResultType(success_type, error_type)
        return self._types[name]
