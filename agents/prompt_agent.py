import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from pathlib import Path

# Load .env from project root
env_path = Path(__file__).resolve().parents[1] / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

def generate_clarifying_questions(context: str) -> list:
    """
    Generate focused clarifying questions for demand forecasting.
    Returns list of questions.
    """
    try:
        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
            messages=[{
                "role": "system",
                "content": """You are a demand forecasting expert. Generate 3-5 specific questions about:
                1. Missing data patterns
                2. Upcoming business events
                3. Market changes
                4. Data anomalies"""
            }, {
                "role": "user",
                "content": f"Data sample:\n{context[:2000]}\nAsk critical questions to improve forecast accuracy:"
            }],
            temperature=0.3,
            max_tokens=300
        )
            # Update return statement to limit questions
        questions = [q.strip() for q in content.split("\n") if q.strip()]
        return questions[:4]  # Maximum 4 questions

        # Extract and format questions
        content = response.choices[0].message.content
        return [q.strip() for q in content.split("\n") if q.strip()]
    
    except Exception as e:
        # Fallback questions
        return [
            "Are there any planned promotions affecting demand?",
            "Will product availability change significantly?",
            "Any known economic factors impacting demand?",
            "Should we adjust for seasonal patterns differently?"
        ]