import logging
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from app.core.config import settings
from app.prompt.prompt import match_template, question_template

logger = logging.getLogger(__name__)


class MatchingService:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name=settings.MODEL,
            base_url=settings.BASE_URL
        )
        
        # Prompt templates
        self.match_prompt = PromptTemplate(input_variables=["resume", "jd"], template=match_template)
        self.question_prompt = PromptTemplate(input_variables=["resume", "jd"], template=question_template)
        
        # Chains
        self.match_chain = LLMChain(llm=self.llm, prompt=self.match_prompt)
        self.question_chain = LLMChain(llm=self.llm, prompt=self.question_prompt)

    def generate_matches(self, resumes: list, jd_text: str) -> list:
        """Generate matches with scores and questions for given resumes."""
        matches = []
        
        for doc in resumes:
            resume_text = doc.page_content
            name = doc.metadata.get("name", "Unknown")

            try:
                match_result = self.match_chain.invoke({"resume": resume_text, "jd": jd_text})
                question_result = self.question_chain.invoke({"resume": resume_text, "jd": jd_text})

                questions = [q.strip() for q in question_result["text"].split("\n") if q.strip()]

                matches.append({
                    "candidate_name": name,
                    "match_score": match_result["text"].strip(),
                    "interview_questions": questions
                })
            except Exception as e:
                logger.error(f"Error generating match for {name}: {e}")
                continue

        return matches