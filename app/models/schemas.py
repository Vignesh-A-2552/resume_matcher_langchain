from pydantic import BaseModel
from typing import List


class UploadResponse(BaseModel):
    message: str


class MatchScore(BaseModel):
    candidate_name: str
    match_score: str
    interview_questions: List[str]


class MatchResponse(BaseModel):
    matches: List[MatchScore]


class ErrorResponse(BaseModel):
    error: str