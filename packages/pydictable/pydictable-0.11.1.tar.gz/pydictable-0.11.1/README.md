# pydictable
Make your classes json serializable and deserializable. It supports **from dict** and **to dict** with proper **attribute hints**. Best usecase would be

1. Let us say you store json in s3. When you fetch it, you want it to be an object instead of a dict.
2. When you want to store the object back to s3, you want to convert it to dict.

NamedTuple would come handy in this situation, but as it is tuple, it is immutable. You can do these two operations easily with DictAble.

### 💾 Installation
```
pip install pydictable
```

### 💡 Example
```python 

class LatLng(DictAble):
    lat: int
    lng: int


class Address(DictAble):
    pin_code: int
    lat_lng: LatLng

class Person(DictAble):
    name: str
    address: Address

input_dict = {
    'name': 'Pramod',
    'address': {
        'pin_code': 560032,
        'lat_lng': {
            'lat': 12345,
            'lng': 67890
        }
    }
}
p = Person(dict=input_dict)
p.name # Pramod
p.address # Address object
p.address.pin_code # 560032

p.to_dict() == input_dict # Not order though!

p.address.pin_code = 518466 # You can change the values

# you can initiate with named params too
p2 = Person(
    name='Pramod',
    address=Address(
        pin_code=560032,
        lat_lng=LatLng(
            lat=12345,
            lng=67890
        )
    )
)
p == p2 # shallow equal
p2.to_dict() == p.to_dict()

# You can get the schema of the modal as well
Person.get_input_schema()
```

### 📜 Supported types
- str
- int
- float
- datetime
- Optional
- Union
- DictAble
- list
- MultiTypeField
```
__init__(self, types: List[Type[DictAble]])
```

- DictValueField
```
__init__(self, dictable_value: Type[DictAble])
```

```
class Car(DictAble):
    name: str = StrField()

class CarA(Car):
    a_field: str = StrField()

class CarB(Car):
    b_field: str = StrField()

class Garage(DictAble):
    cars: List[Car] = ListField(MultiTypeField([CarA, CarB]))
    
class Company(DictAble):
    garbage: Dict[str, Garage] = DictValueField(Garage)


g = Garage(
    cars=[
        CarA(name='i20', a_field='some value')
    ]
)
g.to_dict() # {'cars': [{'a_field': 'some value', 'name': 'i20', '__type': 'CarA'}]}

c = Company(
    garbage={
        'g': Garage(
            cars=[
                CarA(name='i20', a_field='some value')
            ]
        )
    }
)
```

It is still under development. Feel free to report bugs or push changes! Cheers!
