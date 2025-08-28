from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
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
CREATE TABLE IF NOT EXISTS "diaries" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(200) NOT NULL,
    "content" TEXT NOT NULL,
    "emotional_state" VARCHAR(7) NOT NULL DEFAULT 'neutral',
    "emotion_summary" TEXT,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_diaries_title_664dc3" ON "diaries" ("title");
CREATE INDEX IF NOT EXISTS "idx_diaries_emotion_9d873f" ON "diaries" ("emotional_state");
CREATE INDEX IF NOT EXISTS "idx_diaries_created_883a57" ON "diaries" ("created_at");
CREATE INDEX IF NOT EXISTS "idx_diaries_updated_415ddc" ON "diaries" ("updated_at");
CREATE INDEX IF NOT EXISTS "idx_diaries_user_id_12cb33" ON "diaries" ("user_id");
CREATE INDEX IF NOT EXISTS "idx_diaries_user_id_c4acfc" ON "diaries" ("user_id", "created_at");
CREATE INDEX IF NOT EXISTS "idx_diaries_user_id_ce61ef" ON "diaries" ("user_id", "emotional_state");
COMMENT ON COLUMN "diaries"."emotional_state" IS 'neutral: neutral\nhappy: happy\nsad: sad\nangry: angry\nanxious: anxious\nexcited: excited';
COMMENT ON TABLE "diaries" IS 'Diary model';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
