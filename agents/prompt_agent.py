import os
from openai import AzureOpenAI

# Load from environment variables
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Setup AzureOpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

def generate_prompt_clarification(context):
    """
    Ask clarifying questions based on the data context.
    """
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for demand forecasting planners."},
            {"role": "user", "content": f"The user uploaded data:\n{context[:1000]}\nWhat questions would you ask?"}
        ],
        max_tokens=500,
        temperature=0.5
    )
    # ✅ Fix here: access content correctly
    return response.choices[0].message.content
