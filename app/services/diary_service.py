# app/services/diary_service.py

from typing import List

from fastapi import HTTPException, status

from app.models import User
from app.models.diary import Diary, EmotionalState
from app.models.tag import Tag
from app.schemas.diary import DiaryCreate, DiaryOut, DiaryUpdate
from app.services.ai_service import GeminiService


async def create_diary_service(user: User, diary_data: DiaryCreate) -> Diary:
    try:
        print(f"user 타입: {type(user)}, user: {user}")  # 추가
        # emotional_state를 Enum으로 변환
        try:
            emotional_state = EmotionalState(diary_data.emotional_state)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 emotional_state 값입니다.",
            )

        # Diary 인스턴스 생성
        print("Diary 생성 시작")  # 추가
        new_diary = await Diary.create(
            user=user,
            title=diary_data.title,
            content=diary_data.content,
            emotional_state=emotional_state,  # Enum 값 사용
            # ai_summary=diary_data.ai_summary,
        )
        print(f"Diary 생성 완료: {type(new_diary)}")  # 추가

        # 태그 처리
        if diary_data.tags:
            tag_list = []
            for tag_name in diary_data.tags:
                tag, _ = await Tag.get_or_create(name=tag_name)
                tag_list.append(tag)
            await new_diary.tags.add(*tag_list)

        # 태그 관계 포함
        await new_diary.fetch_related("tags")
        return new_diary

    except Exception as e:
        print(f"일기 생성 중 오류 발생: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="일기 생성 중 알 수 없는 오류가 발생했습니다.",
        )


async def get_all_diaries_service(user_id: int) -> List[DiaryOut]:
    diaries = await Diary.filter(user_id=user_id).order_by("-created_at")
    return [DiaryOut.model_validate(d) for d in diaries]


async def get_diary_by_id_service(diary_id: int, user_id: int) -> DiaryOut:
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    return DiaryOut.model_validate(diary)


async def update_diary_service(
    diary_id: int, diary_data: DiaryUpdate, user_id: int
) -> DiaryOut:
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )

    # tags와 emotional_state를 제외한 나머지 필드 업데이트
    # M2M 관계인 tags는 update_from_dict로 업데이트할 수 없음
    update_data = diary_data.model_dump(
        exclude_unset=True, exclude={"tags", "emotional_state"}
    )
    await diary.update_from_dict(update_data)

    # emotional_state 업데이트 (선택적)
    if diary_data.emotional_state:
        try:
            emotional_state = EmotionalState(diary_data.emotional_state)
            diary.emotional_state = emotional_state
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="유효하지 않은 emotional_state 값입니다.",
            )

    # tags 업데이트 (M2M 매니저 사용)
    if diary_data.tags is not None:
        # 기존 태그 관계 삭제
        await diary.tags.clear()

        if diary_data.tags:
            tag_list = []
            for tag_name in diary_data.tags:
                tag, _ = await Tag.get_or_create(name=tag_name)
                tag_list.append(tag)
            await diary.tags.add(*tag_list)

    await diary.save()
    await diary.fetch_related("tags")

    return DiaryOut.model_validate(diary)


async def summarize_diary_service(diary_id: int, user_id: int) -> Diary:
    """
    일기 AI 요약 서비스
    """
    # 일기 조회 및 권한 확인
    diary = await Diary.filter(id=diary_id, user_id=user_id).first()

    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="일기를 찾을 수 없습니다."
        )

    # 이미 요약이 있는 경우 확인
    # if diary.ai_summary:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, detail="이미 요약이 존재합니다."
    #     )

    try:
        # Gemini 서비스로 요약 생성
        gemini_service = GeminiService()
        summary = await gemini_service.summarize_diary(diary.content)

        # 요약 저장
        diary.ai_summary = summary
        await diary.save()

        return diary

    except Exception as e:
        print(f"요약 생성 중 오류: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI 요약 생성에 실패했습니다.",
        )


async def delete_diary_service(diary_id: int, user_id: int):
    diary = await Diary.get_or_none(id=diary_id, user_id=user_id)
    if not diary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 일기를 찾을 수 없거나 권한이 없습니다.",
        )
    await diary.delete()
