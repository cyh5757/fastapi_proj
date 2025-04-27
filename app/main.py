from contextlib import asynccontextmanager
from app.book_scraper import NaverBookScraper
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel

BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongodb.connect()
    try:
        yield
    finally:
        mongodb.close()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # 🔥 검색 결과 없이 검색창만 보여주기 위해 books=None 넘기기
    return templates.TemplateResponse(
        "item.html",
        {
            "request": request,
            "title": "콜렉터 북이",
            "books": None,
        },
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q

    if not keyword:
        context = {
            "request": request,
            "title": "북북이",
        }
        return templates.TemplateResponse("item.html", context)

    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyword == keyword)
        return templates.TemplateResponse(
            "item.html", {"request": request, "title": "북북이", "books": books}
        )

    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, total_page=10)
    book_models = []
    for book in books:
        book_model = BookModel(
            keyword=keyword,
            publisher=book["publisher"],
            price=book["discount"],
            image=book["image"],
            description=book["description"],
        )
        book_models.append(book_model)
    await mongodb.engine.save_all(book_models)
    return templates.TemplateResponse(
        "item.html", {"request": request, "title": "북북이", "books": books}
    )
