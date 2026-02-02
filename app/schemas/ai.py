from pydantic import BaseModel, Field


class AIQuestion(BaseModel):
    question: str = Field(
        ..., min_length=1, max_length=1000, description="Question about the dataset"
    )
    format: str = Field(
        default="plain", description="Response format: 'markdown', 'plain', or 'html'"
    )


class AIAnswer(BaseModel):
    answer: str = Field(..., description="AI generated answer")
    context: str = Field(default="", description="Context used to generate the answer")
    format: str = Field(default="plain", description="Format of the answer")


class DatasetContext(BaseModel):
    cars_count: int
    drivers_count: int
    provinces_count: int
    cities_count: int
    villages_count: int
    sample_cars: list[dict]
    sample_drivers: list[dict]
    sample_provinces: list[dict]
    sample_cities: list[dict]
    sample_villages: list[dict]
