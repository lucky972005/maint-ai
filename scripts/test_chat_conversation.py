import urllib.request
import json

tests = [
    "can you talk normally like also",
    "hi",
    "how are you",
    "who are you",
    "thanks",
    "tell me a joke",
    "im tired today",
    "Why is my motor overheating?",
    "What is the torque spec?",
    "random thought about life",
    "unusual vibration in main hydraulic pump"
]

for t in tests:
    req = urllib.request.Request(
        "http://localhost:3000/api/chat",
        data=json.dumps({"messages": [{"role": "user", "content": t}]}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        msg = data.get("message", "")
        lines = [line.strip() for line in msg.split("\n") if line.strip()]
        first_line = lines[0] if lines else ""
        second_line = lines[1] if len(lines) > 1 else ""
        print(f"QUERY: {t}")
        print(f"  Line 1: {first_line[:80]}")
        print(f"  Line 2: {second_line[:80]}")
        print("-" * 60)
