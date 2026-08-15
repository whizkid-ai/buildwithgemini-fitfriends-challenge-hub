"""Evaluation runner for FitFriends Challenge Hub using local LLM-as-judge."""

import json
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "true")
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-04-6e9778b27cff")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent
from tests.eval.response_quality import evaluate as rate_quality


def run_evaluation():
    dataset_path = Path("tests/eval/datasets/basic-dataset.json")
    if not dataset_path.exists():
        print("Dataset not found!")
        return

    with open(dataset_path) as f:
        data = json.load(f)

    eval_cases = data.get("eval_cases", [])
    session_service = InMemorySessionService()

    results = []
    print(f"\n================ Running Eval for {len(eval_cases)} cases ================\n")

    for idx, case in enumerate(eval_cases, 1):
        case_id = case.get("eval_case_id", f"case_{idx}")
        prompt_text = case["prompt"]["parts"][0]["text"]
        print(f"[{idx}/{len(eval_cases)}] Case '{case_id}': \"{prompt_text}\"")

        session = session_service.create_session_sync(user_id="eval_user", app_name="eval_app")
        runner = Runner(agent=root_agent, session_service=session_service, app_name="eval_app")

        msg = types.Content(role="user", parts=[types.Part.from_text(text=prompt_text)])
        events = list(runner.run(new_message=msg, user_id="eval_user", session_id=session.id))

        # Extract model text or A2UI content from all events
        text_parts = []
        for event in events:
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        text_parts.append(part.text)
                    elif part.inline_data and part.inline_data.data:
                        try:
                            decoded = part.inline_data.data.decode("utf-8")
                            text_parts.append(f"[A2UI Rendered Card Data: {decoded[:200]}...]")
                        except Exception:
                            pass

        final_text = "\n".join(text_parts).strip() if text_parts else "No response generated."

        # Grade using response_quality
        instance = {
            "prompt": prompt_text,
            "response": final_text,
            "reference": case.get("reference", ""),
            "agent_data": f"Events count: {len(events)} | Parts count: {len(text_parts)}",
        }
        verdict = rate_quality(instance)
        print(f"   -> Response preview: {final_text[:120]}...")
        print(f"   -> Score: {verdict['score']}/5 | Explanation: {verdict['explanation']}\n")

        results.append({
            "case_id": case_id,
            "prompt": prompt_text,
            "response": final_text,
            "score": verdict["score"],
            "explanation": verdict["explanation"],
        })

    avg_score = sum(r["score"] for r in results) / len(results) if results else 0
    print("================ Evaluation Results Summary ================")
    for r in results:
        print(f"• {r['case_id']}: {r['score']}/5 - {r['explanation']}")
    print(f"\nOverall Average Quality Score: {avg_score:.2f} / 5.0")


if __name__ == "__main__":
    run_evaluation()
