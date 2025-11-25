import asyncio
from app.db.logic import AsyncSessionLocal
from app.services.shortener import shorten_url

async def test():
    async with AsyncSessionLocal() as db:
        url = "https://www.amazon.in/Adjustable-Strengthener-Mechanical-Resistance-Workouts/dp/B0FDB3JPVM/?_encoding=UTF8&ref_=pd_hp_d_atf_dealz_cs"
        result = await shorten_url(db, url, "handgripper", 11)
        print(f"\nThe shortened URL is: {result.short_code}")
        print(f"\nThe original url was: {result.original_url}")
        
if __name__ == '__main__':
    asyncio.run(test())

