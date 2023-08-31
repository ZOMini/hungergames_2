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
