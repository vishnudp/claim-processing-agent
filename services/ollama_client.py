import json
import time
import traceback

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def generate(
    prompt,
    model="qwen3:4b",
    timeout=300
):

    start = time.time()

    print("=" * 80)
    print(f"Calling Ollama Model : {model}")
    print("=" * 80)

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0,
            "num_predict": 300
        },
        "think": False,
        "format": "json",
    }

    try:

        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=timeout
        )

        elapsed = time.time() - start

        print(
            f"Ollama completed in {elapsed:.2f} sec"
        )

        response.raise_for_status()

        data = response.json()

        # print("\nOLLAMA RESPONSE")
        # print(json.dumps(data, indent=4)[:2000])


        # Qwen3 puts output in thinking field
        # when reasoning mode is enabled
        result = data.get("response")


        if not result:

            result = data.get("thinking")


        if not result:

            raise ValueError(
                "Ollama returned empty response"
            )


        print("\nMODEL OUTPUT")
        print(result)

        return result


    except Exception:

        traceback.print_exc()
        raise