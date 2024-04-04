from pydantic import BaseModel

from core.constants import DefaultImagePath


class OptionData(BaseModel):
    id: str
    text: str


class QuestionData(BaseModel):
    id: str
    title: str
    description: str
    options: list[OptionData]
    image: str = DefaultImagePath.question.value


class QuizData(BaseModel):
    name: str
    description: str
    opening_image_path: str = DefaultImagePath.quiz.value
    closing_image_path: str = DefaultImagePath.ps.value
    ps_text: str | None
    ps_url: str | None
    question: QuestionData | None = None


class AnswerData(BaseModel):
    option_id: int
