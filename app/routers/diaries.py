from fastapi import APIRouter, HTTPException

from app.models.diaries import Diary
from app.schemas.diary import (
    DiaryCreate,
    DiaryOut,
    DiaryUpdate,
)
from app.services.diary_service import DiaryService

router = APIRouter(prefix="/diaries", tags=["diaries"])
service = DiaryService()


@router.post("/", response_model=DiaryOut)
async def create_diary(diary_create: DiaryCreate):
    from app.models import User

    user = await User.get_or_none(id=diary_create.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    diary = await Diary.create(**diary_create.model_dump())
    return DiaryOut.model_validate(diary)


# READ ALL
@router.get("/", response_model=List[DiaryOut])
async def list_diaries():
    diaries = await Diary.all()
    return [DiaryOut.model_validate(d) for d in diaries]


# READ ONE
@router.get("/{diary_id}", response_model=DiaryOut)
async def get_diary(diary_id: int):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")
    return DiaryOut.model_validate(diary)


# UPDATE
@router.put("/{diary_id}", response_model=DiaryOut)
async def update_diary(diary_id: int, diary_update: DiaryUpdate):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    update_data = diary_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(diary, key, value)
    await diary.save()

    return DiaryOut.model_validate(diary)


# DELETE
@router.delete("/{diary_id}", response_model=dict)
async def delete_diary(diary_id: int):
    diary = await Diary.get_or_none(id=diary_id)
    if not diary:
        raise HTTPException(status_code=404, detail="Diary not found")

    await diary.delete()
    return {"detail": "Diary deleted successfully"}
