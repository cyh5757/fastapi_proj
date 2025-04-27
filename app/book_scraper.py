import asyncio
from app.config import get_secret
import aiohttp


class NaverBookScraper:

    Naver_API_BOOK = "https://openapi.naver.com/v1/search/book"
    NAVER_API_ID = get_secret("Naver_API_ID")
    NAVER_API_SECRET = get_secret("Naver_API_SECRET")

    @staticmethod
    async def fetch(session, url, headers):
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                result = await response.json()
                return result["items"]
            else:
                print(f"Error: {response.status}")
                return None

    def unit_url(self, keyword, start):
        return {
            "url": f"{self.Naver_API_BOOK}?query={keyword}&display=10&start={start}",
            "headers": {
                "X-Naver-Client-Id": self.NAVER_API_ID,
                "X-Naver-Client-Secret": self.NAVER_API_SECRET,
            },
        }

    async def search(self, keyword, total_page):
        apis = [self.unit_url(keyword, 1 + i * 10) for i in range(total_page)]
        async with aiohttp.ClientSession() as session:
            results = await asyncio.gather(
                *[self.fetch(session, api["url"], api["headers"]) for api in apis]
            )
            result = []
            for data in results:
                if data is not None:
                    for book in data:
                        result.append(book)
            return result

    def run(self, keyword, total_page):
        return asyncio.run(self.search(keyword, total_page))


if __name__ == "__main__":
    scraper = NaverBookScraper()
    results = scraper.run("파이썬", 2)
    print(results)
    print(len(results))
