import sys
import os

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.prompt_agent import generate_prompt_clarification  # <-- Corrected import ✅

if __name__ == "__main__":
    stage = "Demand Segmentation"
    context = "We just clustered SKUs using volatility and seasonality"

    suggestion = generate_prompt_clarification(context)  # <-- Corrected call ✅
    print("🤖 Suggested prompt:")
    print(suggestion)
