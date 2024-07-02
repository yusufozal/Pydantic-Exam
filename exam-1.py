import pydantic # veri modellemesi için
import json # JSON işlemleri için
from typing import Optional,List #  tip ipuçları için kullanılır.

class ISBNMissingError(Exception):
    """Custom error that is raised when both ISBN10 and ISBN13 are missing."""

    def __init__(self, title: str, message: str) -> None:
        self.title = title
        self.message = message
        super().__init__(message)

class ISBN10FormatError(Exception):
    """Custom error that is raised when ISBN10 doesn't have the right format."""

    def __init__(self, value: str, message: str) -> None:
        self.value = value
        self.message = message
        super().__init__(message)

class Author(pydantic.BaseModel):
    name: str
    verified: bool

class Book(pydantic.BaseModel): # Book adında bir Pydantic modeli tanımlar
    title: str
    author: str
    publisher: str
    price: float
    isbn_10: Optional[str] = None # Modelin isteğe bağlı alanlarını tanımlar.
    isbn_13: Optional[str] = None #  Optional kullanılarak bu alanların boş olabileceği belirtilir.
    subtitle: Optional[str] = None
    author2: Optional[Author] =None


@pydantic.root_validator(pre=True)
@classmethod
def check_isbn_10_or_13(cls, values):
    """Make sure there is either an isbn_10 or isbn_13 value defined"""
    if "isbn_10" not in values and "isbn_13" not in values:
        raise ISBNMissingError(
            title=values["title"],
            message="Document should have either an ISBN10 or ISBN13",
        )
    return values






def main() -> None:
    try:
        with open("./data.json") as file: # "data.json" adında bir dosya açar.
            data = json.load(file) # JSON dosyasının içeriğini Python nesnesine dönüştürür.
            books: List[Book] = [Book(**item) for item in data] # JSON verisindeki her öğeyi Book nesnesine dönüştürür ve bunları bir liste içinde saklar.
            print(books[0].title)
    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()