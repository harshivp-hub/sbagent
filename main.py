import os
import json
from dotenv import load_dotenv
from orchestrator.orchestrator import Orchestrator

# Load env vars
load_dotenv()
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

def main(input_path: str, output_path: str):
    data = json.load(open(input_path))
    orch = Orchestrator()
    result = orch.run(data)
    with open(output_path, "w") as f:
        f.write(result.json(indent=2))
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python main.py <input.json> <output.json>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
