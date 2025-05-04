import os
from pathlib import Path
from dotenv import load_dotenv  # NEW
from openai import AzureOpenAI

# ========== NEW: Load .env file ==========
env_path = Path(__file__).resolve().parents[1] / ".env"  # Path to root .env
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    raise EnvironmentError("🔴 .env file not found in project root! Path tried: " + str(env_path))

# ========== Azure Client Setup ==========
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),       # Directly use os.getenv
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),               # Instead of variables
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

def generate_summary(rows, columns, clusters, models):
    """
    Summarize the entire forecasting session based on given metrics.
    """
    try:
        model_list = ", ".join(set(models.values())) if models else "Unknown models"

        context = (
            f"In this forecasting session:\n"
            f"- {rows} rows and {columns} columns were processed.\n"
            f"- The data was segmented into {clusters} clusters.\n"
            f"- Models selected: {model_list}.\n"
            f"- Forecasts were generated and finalized."
        )

        response = client.chat.completions.create(
            model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),  # Direct from .env
            messages=[
                {"role": "system", "content": "You are a summarization assistant."},
                {"role": "user", "content": f"Summarize this session briefly:\n{context}"}
            ],
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Summary generation failed: {str(e)}"  # Error handling