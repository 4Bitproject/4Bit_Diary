from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "diary" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "emotional_state" VARCHAR(7) NOT NULL,
    "ai_summary" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON COLUMN "diary"."emotional_state" IS 'HAPPY: happy\nSAD: sad\nANGRY: angry\nNEUTRAL: neutral';
CREATE TABLE IF NOT EXISTS "emotion_keyword" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "emotion_keyword" VARCHAR(50) NOT NULL,
    "emotion_type" VARCHAR(20) NOT NULL
);
COMMENT ON COLUMN "emotion_keyword"."emotion_type" IS 'positive: positive\nnegative: negative\nneutral: neutral';
CREATE TABLE IF NOT EXISTS "tag" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "tokenblacklist" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "jti" VARCHAR(36) NOT NULL UNIQUE,
    "exp" TIMESTAMPTZ NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    "nickname" VARCHAR(50) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "phone_number" VARCHAR(20),
    "last_login" TIMESTAMPTZ,
    "is_staff" BOOL NOT NULL DEFAULT False,
    "is_admin" BOOL NOT NULL DEFAULT False,
    "is_active" BOOL NOT NULL DEFAULT True,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
