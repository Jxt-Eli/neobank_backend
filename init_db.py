print("WARNING: THIS FILE IS NO LONGER IN USE!!!")
# import asyncio
# from database import engine
# from models import Base
#
# async def init_db():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)     # NOTE: CHANGING AS SOON AS I LEARN MIGRATIONS
#         await conn.run_sync(Base.metadata.create_all) # WARNING: THIS ISNT DONE ANYWHERE IN PRODUCTION READY CODE AS IT CLEARS ALL DATA 
#     print("✅ Database tables created!")
#
# if __name__ == "__main__":
#     asyncio.run(init_db())
