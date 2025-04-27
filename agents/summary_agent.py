import os
from openai import AzureOpenAI

# Azure OpenAI settings
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

def generate_summary(rows, columns, clusters, models):
    """
    Summarize the entire forecasting session based on given metrics.
    """
    model_list = ", ".join(set(models.values())) if models else "Unknown models"

    # 👇 Create a readable session description
    context = (
        f"In this forecasting session:\n"
        f"- {rows} rows and {columns} columns were processed.\n"
        f"- The data was segmented into {clusters} clusters.\n"
        f"- Models selected for forecasting: {model_list}.\n"
        f"- Forecasts were generated and finalized."
    )

    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a summarization assistant for demand forecasting."},
            {"role": "user", "content": f"Summarize this forecasting session briefly:\n{context}"}
        ],
        max_tokens=300,
        temperature=0.5
    )
    return response.choices[0].message.content
