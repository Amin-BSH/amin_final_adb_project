import json
import os
import re

from dotenv import load_dotenv
from openai import OpenAI
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.car import Car
from app.models.city import City
from app.models.driver import Driver
from app.models.province import Province
from app.models.village import Village

load_dotenv()


class AIAssistantService:
    """Service for AI-powered Q&A about the dataset"""

    def __init__(self):
        self.client = OpenAI(
            base_url=os.getenv("LIARA_BASE_URL"),
            api_key=os.getenv("LIARA_API_KEY", ""),
        )
        self.model = "openai/gpt-4o-mini"

    async def get_dataset_context(self, session: Session) -> dict:
        """Gather dataset statistics and sample data for context"""

        # Get counts
        cars_result = await session.execute(select(func.count(Car.id)))
        cars_count = cars_result.scalar() or 0

        drivers_result = await session.execute(select(func.count(Driver.id)))
        drivers_count = drivers_result.scalar() or 0

        provinces_result = await session.execute(select(func.count(Province.id)))
        provinces_count = provinces_result.scalar() or 0

        cities_result = await session.execute(select(func.count(City.id)))
        cities_count = cities_result.scalar() or 0

        villages_result = await session.execute(select(func.count(Village.id)))
        villages_count = villages_result.scalar() or 0

        # Get sample data (limit to 3 per table)
        cars_query = await session.execute(select(Car).limit(3))
        cars = [
            {
                "id": car.id,
                "name": car.name,
            }
            for car in cars_query.scalars().all()
        ]

        drivers_query = await session.execute(select(Driver).limit(3))
        drivers = [
            {
                "id": driver.id,
                "name": driver.name,
                "last_name": driver.last_name,
                "national_code": driver.national_code,
                "phone_number": driver.phone_number,
                "license_plate": driver.license_plate,
                "capacity_ton": driver.capacity_ton,
                "car_id": driver.car_id,
            }
            for driver in drivers_query.scalars().all()
        ]

        provinces_query = await session.execute(select(Province).limit(3))
        provinces = [
            {"id": p.id, "name": p.province} for p in provinces_query.scalars().all()
        ]

        cities_query = await session.execute(select(City).limit(3))
        cities = [
            {"id": c.id, "name": c.city, "province": c.province_id}
            for c in cities_query.scalars().all()
        ]

        villages_query = await session.execute(select(Village).limit(3))
        villages = [
            {"id": v.id, "name": v.village, "city": v.city_id}
            for v in villages_query.scalars().all()
        ]

        return {
            "cars_count": cars_count,
            "drivers_count": drivers_count,
            "provinces_count": provinces_count,
            "cities_count": cities_count,
            "villages_count": villages_count,
            "sample_cars": cars,
            "sample_drivers": drivers,
            "sample_provinces": provinces,
            "sample_cities": cities,
            "sample_villages": villages,
        }

    async def answer_question(self, question: str, session: Session) -> tuple[str, str]:
        """
        Answer a question about the dataset using AI.

        Returns:
            tuple: (answer, context_summary)
        """
        # Get dataset context
        context = await self.get_dataset_context(session)

        # Prepare context summary for the user
        context_summary = (
            f"Database contains: {context['cars_count']} cars, "
            f"{context['drivers_count']} drivers, "
            f"{context['provinces_count']} provinces, "
            f"{context['cities_count']} cities, "
            f"{context['villages_count']} villages"
        )

        # Prepare system prompt with dataset information
        system_prompt = f"""You are an AI assistant that ONLY answers questions based on the provided dataset.

IMPORTANT RULES:
1. You MUST ONLY use information from the dataset provided below
2. You MUST NOT provide any general knowledge or information outside the dataset
3. If a question cannot be answered using ONLY the dataset information, you MUST respond with: "This information is not available in the dataset.
or "این اطلاعات در مجموعه داده موجود نیست." (based on the question language)
4. Do NOT provide any additional context, facts, or knowledge beyond what is in the dataset
5. Respond in the same language as the question (Persian or English)

Database Overview:
- Total Cars: {context["cars_count"]}
- Total Drivers: {context["drivers_count"]}
- Total Provinces: {context["provinces_count"]}
- Total Cities: {context["cities_count"]}
- Total Villages: {context["villages_count"]}

Sample Data Available:
- Cars: {json.dumps(context["sample_cars"], ensure_ascii=False)}
- Drivers: {json.dumps(context["sample_drivers"], ensure_ascii=False)}
- Provinces: {json.dumps(context["sample_provinces"], ensure_ascii=False)}
- Cities: {json.dumps(context["sample_cities"], ensure_ascii=False)}
- Villages: {json.dumps(context["sample_villages"], ensure_ascii=False)}"""

        # Call AI API
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question},
                ],
                temperature=0.7,
                max_tokens=500,
            )

            answer = completion.choices[0].message.content
            return answer, context_summary
        except Exception as e:
            raise Exception(f"AI service error: {str(e)}")

    def markdown_to_plain(self, markdown_text: str) -> str:
        """Convert Markdown to plain text"""
        # Replace bold (**text**)
        text = re.sub(r"\*\*(.+?)\*\*", r"\1", markdown_text)
        # Replace italic (*text*)
        text = re.sub(r"\*(.+?)\*", r"\1", text)
        # Replace code (`text`)
        text = re.sub(r"`(.+?)`", r"\1", text)
        # Replace headers (## text -> text)
        text = re.sub(r"#{1,6}\s+", "", text)
        # Replace bullet points (- text -> • text)
        text = re.sub(r"^\s*-\s+", "• ", text, flags=re.MULTILINE)
        # Replace numbered lists
        text = re.sub(r"^\s*\d+\.\s+", "", text, flags=re.MULTILINE)
        # Clean up multiple newlines
        text = re.sub(r"\n\n+", "\n\n", text)
        return text.strip()

    def markdown_to_html(self, markdown_text: str) -> str:
        """Convert Markdown to HTML"""
        text = markdown_text
        # Headers
        text = re.sub(r"^### (.+)$", r"<h3>\1</h3>", text, flags=re.MULTILINE)
        text = re.sub(r"^## (.+)$", r"<h2>\1</h2>", text, flags=re.MULTILINE)
        text = re.sub(r"^# (.+)$", r"<h1>\1</h1>", text, flags=re.MULTILINE)
        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # Italic
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        # Code
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        # Paragraphs
        text = re.sub(r"\n\n+", "</p><p>", text)
        text = f"<p>{text}</p>"
        # Lists
        text = re.sub(r"<p>• (.+?)</p>", r"<li>\1</li>", text)
        text = re.sub(r"(<li>.+?</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)
        # Line breaks
        text = text.replace("\n", "<br>")
        return text

    def format_response(self, answer: str, format_type: str = "plain") -> str:
        """Format the answer based on requested format"""
        if format_type == "html":
            return self.markdown_to_html(answer)
        elif format_type == "plain":
            return self.markdown_to_plain(answer)
        else:  # markdown (default)
            return answer


# Create singleton instance
ai_service = AIAssistantService()
