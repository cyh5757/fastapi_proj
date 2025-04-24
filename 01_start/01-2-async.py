import time
import asyncio


async def delivery(name, mealtime):
    print(f"{name} 식사 시작")
    await asyncio.sleep(mealtime)
    print(f"{name} 식사 끝")
    return f"{name} {mealtime} 시간 식사 완료"


async def main():
    await asyncio.gather(
        delivery("영훈", 3),
        delivery("철수", 4),
        delivery("영수", 2),
    )


if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"총 식사 시간: {end - start}")
