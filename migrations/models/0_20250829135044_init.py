from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "nickname" VARCHAR(50) NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "phone_number" VARCHAR(20),
    "last_login" TIMESTAMP,
    "is_staff" INT NOT NULL DEFAULT 0,
    "is_admin" INT NOT NULL DEFAULT 0,
    "is_active" INT NOT NULL DEFAULT 1,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "tokenblacklist" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "jti" VARCHAR(36) NOT NULL UNIQUE,
    "exp" TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS "diary" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "user_id" INT NOT NULL,
    "title" VARCHAR(100) NOT NULL,
    "content" TEXT NOT NULL,
    "emotional_state" VARCHAR(7) /* HAPPY: happy\nSAD: sad\nANGRY: angry\nNEUTRAL: neutral */,
    "ai_summary" TEXT,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "tag" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(50) NOT NULL
);
CREATE TABLE IF NOT EXISTS "diary_tags" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "diary_id" INT NOT NULL REFERENCES "diary" ("id") ON DELETE CASCADE,
    "tag_id" INT NOT NULL REFERENCES "tag" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_diary_tags_diary_i_cf5d22" UNIQUE ("diary_id", "tag_id")
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
