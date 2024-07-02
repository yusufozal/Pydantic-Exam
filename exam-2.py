import pydantic
import pydantic_settings


class User:
    def __init__(self, id, name='Jane Doe'):
        if not isinstance(id, int):
            raise TypeError(f'Expected id to be an int, got {type(id).__name__}')

        if not isinstance(name, str):
            raise TypeError(f'Expected name to be a str, got {type(name).__name__}')

        self.id = id
        self.name = name


try:
    user = User(id='123')
except TypeError as e:
    print(e)

from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str = 'Jane Doe'
""""
user=User(id='123')
print(user.id)
print(user.model_fields_set)
user=User(id='123', name='Jane Doe')
print(user.model_fields_set)
print(user.model_dump())
print(user.model_dump_json())
print(user.model_json_schema())
"""
from  typing import List,Optional

class food(BaseModel):
    name: str
    price: float
    ingredients: Optional[List[str]] = None

class Restaurant(BaseModel):
    name: str
    location: str
    foods: List[food]


restaurant_instance = Restaurant(
    name="Tasty Bites",
    location="123, Flavor Street",
    foods=[
        {"name": "Cheese Pizza", "price": 12.50, "ingredients": ["Cheese", "Tomato Sauce", "Dough"]},
        {"name": "Veggie Burger", "price": 8.99}
    ]
)
#print(restaurant_instance)
#print(restaurant_instance.model_dump())
from pydantic import BaseModel, EmailStr, PositiveInt, conlist, Field, HttpUrl

from typing import List
from pydantic import BaseModel, EmailStr, PositiveInt, conlist, Field, HttpUrl


class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str


class Employee(BaseModel):
    name: str
    position: str
    email: EmailStr


class Owner(BaseModel):
    name: str
    email: EmailStr


class Restaurant(BaseModel):
    name: str = Field(..., pattern=r"^[a-zA-Z0-9-' ]+$")
    owner: Owner
    address: Address
    employees: conlist(Employee, min_length=2)
    number_of_seats: PositiveInt
    delivery: bool
    website: HttpUrl


# Creating an instance of the Restaurant class
restaurant_instance = Restaurant(
    name="Tasty Bites",
    owner={
        "name": "John Doe",
        "email": "john.doe@example.com"
    },
    address={
        "street": "123, Flavor Street",
        "city": "Tastytown",
        "state": "TS",
        "zip_code": "12345",
    },
    employees=[
        {
            "name": "Jane Doe",
            "position": "Chef",
            "email": "jane.doe@example.com"
        },
        {
            "name": "Mike Roe",
            "position": "Waiter",
            "email": "mike.roe@example.com"
        }
    ],
    number_of_seats=50,
    delivery=True,
    website="http://tastybites.com"
)


#print(restaurant_instance)
from pydantic import BaseModel, EmailStr, field_validator
class Owner(BaseModel):
    name: str
    email: EmailStr

    @field_validator('name')
    @classmethod
    def name_must_contain_space(cls, v: str) -> str:
        if ' ' not in v:
            raise ValueError('Owner name must contain a space')
        return v.title()


try:
    owner_instance = Owner(name="JohnDoe", email="john.doe@example.com")
except ValueError as e:
    #print(e)

    from typing import Any
    from pydantic import BaseModel, EmailStr, ValidationError, model_validator


    class Owner(BaseModel):
        name: str
        email: EmailStr

        @model_validator(mode='before')
        @classmethod
        def check_sensitive_info_omitted(cls, data: Any) -> Any:
            if isinstance(data, dict):
                if 'password' in data:
                    raise ValueError('password should not be included')
                if 'card_number' in data:
                    raise ValueError('card_number should not be included')
            return data

        @model_validator(mode='after')
        def check_name_contains_space(self) -> 'Owner':
            if ' ' not in self.name:
                raise ValueError('Owner name must contain a space')
            return self


   # print(Owner(name="John Doe", email="john.doe@example.com"))

    try:
        Owner(name="JohnDoe", email="john.doe@example.com", password="password123")
    except ValidationError as e:
       # print(e)

       from pydantic import BaseModel, Field



from pydantic import BaseModel, Field

class User(BaseModel):
    name: str = Field(default='John Doe')

user = User()
#print(user)

from uuid import uuid4

from pydantic import BaseModel, Field

class User(BaseModel):
    id: int = Field(default_factory=lambda: uuid4().hex)

user = User()
#print(user)



from pydantic import BaseModel, Field


class User(BaseModel):
    name: str = Field(..., alias='username')


user = User(username='johndoe')
#print(user)
#print(user.model_dump(by_alias=True))

from typing import List
from pydantic import BaseModel, Field, EmailStr
from decimal import Decimal

class User(BaseModel):
    username: str = Field(..., min_length=3, max_length=10, pattern=r'^\w+$')
    email: EmailStr = Field(...)
    age: int = Field(..., gt=0, le=120)
    height: float = Field(..., gt=0.0)
    is_active: bool = Field(True)
    balance: Decimal = Field(..., max_digits=10, decimal_places=2)
    favorite_numbers: List[int] = Field(..., min_items=1)

user_instance = User(
    username="john_doe",
    age=30,
    height=5.9,
    weight=160.5,
    email="john.doe@example.com",
    password="securepassword",
    balance=9999.99,
    favorite_numbers=[1,2,3]
)

#

from pydantic import BaseModel, computed_field
from datetime import datetime


class Person(BaseModel):
    name: str
    birth_year: int

    @computed_field
    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year


#print(Person(name="John Doe", birth_year=2002).model_dump())

from pydantic import BaseModel, ValidationError, field_validator
from datetime import datetime

class Person(BaseModel):
    name: str
    birth_year: int

    @property
    def age(self) -> int:
        current_year = datetime.now().year
        return current_year - self.birth_year

    @field_validator('birth_year')
    @classmethod
    def validate_age(cls, v: int) -> int:
        current_year = datetime.now().year
        if current_year - v < 18:
            raise ValueError('Person must be 18 years or older')
        return v
""" 
try:
    print(Person(name="John Doe", birth_year=2010))
except ValidationError as e:
     print(e)


import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_key: str = Field(validation_alias='my_auth_key')
    api_key: str = Field(alias='my_api_key')


#print(Settings().model_dump())

import os
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings

os.environ["AUTH_KEY"] = "test_auth_key"
os.environ["MY_API_KEY"] = "test"
os.environ["ENV2"] = "https://mysuperurl.com"


class Settings(BaseSettings):
    service_name: str = Field(default="default")
    auth_key: str
    api_key: str = Field(alias='my_api_key')
    url: str = Field(validation_alias=AliasChoices("env1", "env2"))


print(Settings().model_dump())
"""
import os
from pydantic import Field,AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

# Set environment variables with the prefix
os.environ["PRODUCTION_AUTH_KEY"] = "test_auth_key"
os.environ["PRODUCTION_MY_API_KEY"] = "test"
os.environ["PRODUCTION_ENV2"] = "https://mysuperurl.com"

os.environ["AUTH_KEY"] = "test_auth_key"
os.environ["MY_API_KEY"] = "test"
os.environ["ENV2"] = "https://mysuperurl.com"


class Settings(BaseSettings):
    service_name: str = Field(default="default")
    auth_key: str
    api_key: str = Field(alias='my_api_key')
    url: str = Field(validation_alias=AliasChoices("env1", "env2"))


print(Settings().model_dump())

