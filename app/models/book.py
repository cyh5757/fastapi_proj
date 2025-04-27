from odmantic import Model
from typing import Optional

# DB(fastapi-pj) -> collection books ->
# documnet{
#     keyword: "파이썬",
#     publisher: "출판사",
#     price: 10000,
#     image: "이미지 주소",
# }


class BookModel(Model):
    keyword: str
    publisher: str
    price: int
    image: str
    description: Optional[str] = None

    __collection__ = "books"
