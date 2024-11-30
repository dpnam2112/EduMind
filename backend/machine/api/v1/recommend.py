from typing import List
from core.response import Ok
from machine.models import *
from fastapi import APIRouter, Depends
from machine.schemas.requests import *
from machine.schemas.responses.recommend import *
from machine.controllers import *
from machine.providers import InternalProvider
from core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/recommend_lessons", tags=["recomendation"])


@router.get("/{recommendLessonId}", response_model=Ok[RecommendLessonResponse])
async def recommend_lesson(
    recommendLessonId: UUID,
    lessons_controller: LessonsController = Depends(InternalProvider().get_lessons_controller),
):
   
    # Fetch the lesson recommendation details
    lesson = await lessons_controller.lessons_repository.first(
        where_=[Lessons.id == recommendLessonId],
        relations=[Lessons.modules],
    )

    if not lesson:
        raise NotFoundException(message="Lesson not found for the given ID.")

    response_data = RecommendLessonResponse(
        lesson_id=lesson.id,
        name=lesson.title,
        learning_outcomes=[outcome for outcome in lesson.learning_outcomes],
        description=lesson.description,
        progress=lesson.progress,
        status=lesson.status,
        recommend_content=lesson.recommended_content,
        explain=lesson.explain,
        modules=[
            ModuleResponse(
                module_id=module.id,
                title=module.title,
            )
            for module in lesson.modules
        ],
    )

    return Ok(data=response_data, message="Successfully fetched the recommended lesson.")