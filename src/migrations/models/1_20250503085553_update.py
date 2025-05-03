from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" ADD "response" VARCHAR(1000);
        ALTER TABLE "orders" ADD "question" VARCHAR(500);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "orders" DROP COLUMN "response";
        ALTER TABLE "orders" DROP COLUMN "question";"""
