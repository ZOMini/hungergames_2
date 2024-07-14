from pydantic import BaseModel


class SubB(BaseModel):
    b1: str
    b2: str


class SubC(BaseModel):
    __root__: list[SubB]

    def __init__(self, **data):
        for n, i in enumerate(data['__root__']):
            if i['b1'] != 'qq':
                del data['__root__'][n]
        super().__init__(**data)


class A(BaseModel):
    a1: str
    a2: str
    # sub_b: SubB
    sub_c: SubC


_dict = {'a1': 'qq', 'a2': 'qq', 'sub_c': [{'b1': 'qq', 'b2': 'qq'}, {'b1': 'qq2', 'b2': 'qq2'}]}
_a = A(**_dict)
print(_a.dict())

from types import FunctionType, MethodType

def check_func_or_method(obj):
    if isinstance(obj, (FunctionType, MethodType)): # if callable
        name = obj.__code__.co_name
        print ('callable object -', name, '- him args:')
        only_args = [x for x in obj.__code__.co_varnames if x not in ('cls', 'self')]
        diff = len(only_args) - len(obj.__defaults__) if obj.__defaults__ else 0
        for n, name in enumerate(only_args):
            annotation = obj.__annotations__.get(name, '<no annotation>') if obj.__annotations__ else '<no annotation>'
            default = obj.__defaults__[n - 1 - diff] if obj.__defaults__ and diff <= n else '<no default>'
            print (f'{name}: {annotation} = {default}')
    elif isinstance(obj, type):
        print(f'Класс {obj.__name__}, '
              f'свойства: {[x for x in dir(obj) if not callable(getattr(obj, x)) and not x.startswith("__")]}, '
              f'методы {[x for x in dir(obj) if callable(getattr(obj, x)) and not x.startswith("__")]}.')
    elif hasattr(obj, '__dict__'):
        print(f'Объект класса OracleHelper, '
              f'свойства: {[x for x in dir(obj) if not callable(getattr(obj, x)) and not x.startswith("__")]}, '
              f'методы {[x for x in dir(obj) if callable(getattr(obj, x)) and not x.startswith("__")]}.')
    else:
        print('')

# примеры:
class OracleHelper:
    def __init__(self):
        self.arg_1 = '1'
        self.arg_2 = '2'
        self.arg_3 = '3'
        self.arg_1_2_3 = self.arg_1 + self.arg_2 + self.arg_3

    @property
    def get_123(self):
        return self.arg_1_2_3

    def get_321(self, q3: int, q4, q5, q1: str = 'zzzzzzzzzzzzzzzzzzzzzzzzzzzz', q2: str = '22'):
        return q1 + q2

    def __str__(self) -> str:
        return (f'Объект класса OracleHelper, '
                f'свойства: {[x for x in self.__dir__() if not callable(getattr(self, x)) and not x.startswith("__")]}, '
                f'методы {[x for x in self.__dir__() if callable(getattr(self, x)) and not x.startswith("__")]}.')


def print_funk_args(fn, fn1, fn2 = 111):
    print(locals())

oh = OracleHelper()

check_func_or_method(print_funk_args) # Чекаем функцию
check_func_or_method(oh.get_321) # Метод класса/объекта
check_func_or_method(OracleHelper()) # Объект
check_func_or_method(OracleHelper) # Класс
