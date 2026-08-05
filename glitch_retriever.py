import json
from pathlib import Path


DATA_PATH = (
    Path(__file__).resolve().parent
    / "data"
    / "glitch_knowledge.json"
)


def load_knowledge_base():
    """Load troubleshooting records from the JSON knowledge base."""
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def classify_glitch(description):
    """Classify the glitch using keyword matches from the knowledge base."""
    text = description.lower()
    records = load_knowledge_base()

    scores = {}

    for record in records:
        category = record["category"]
        matches = sum(
            1 for keyword in record["keywords"]
            if keyword.lower() in text
        )

        scores[category] = scores.get(category, 0) + matches

    if not scores or max(scores.values()) == 0:
        return "unknown"

    return max(scores, key=scores.get)


def retrieve_matches(description, platform, top_k=3):
    """Retrieve and rank the most relevant troubleshooting records."""
    text = description.lower()
    category = classify_glitch(description)
    records = load_knowledge_base()
    ranked_results = []

    for record in records:
        platform_match = (
            platform in record["platforms"]
            or "All" in record["platforms"]
        )

        if not platform_match:
            continue

        keyword_matches = sum(
            1 for keyword in record["keywords"]
            if keyword.lower() in text
        )

        category_match = int(record["category"] == category)

        retrieval_score = (
            keyword_matches * 3
            + category_match * 2
            + 1
        )

        if retrieval_score > 1:
            ranked_results.append(
                {
                    **record,
                    "retrieval_score": retrieval_score,
                    "keyword_matches": keyword_matches,
                }
            )

    ranked_results.sort(
        key=lambda item: item["retrieval_score"],
        reverse=True,
    )

    return ranked_results[:top_k]


def calculate_confidence(description, retrieved_results):
    """Return a confidence score from 0.0 to 1.0."""
    if not description.strip():
        return 0.0

    if not retrieved_results:
        return 0.2

    top_result = retrieved_results[0]
    keyword_score = min(top_result["keyword_matches"] / 3, 1.0)
    retrieval_score = min(top_result["retrieval_score"] / 10, 1.0)

    confidence = (
        keyword_score * 0.5
        + retrieval_score * 0.5
    )

    return round(confidence, 2)


def build_diagnosis(description, platform):
    """Create a structured diagnosis using retrieved knowledge."""
    if not isinstance(description, str) or not description.strip():
        return {
            "status": "rejected",
            "message": "Please describe the game glitch.",
        }

    if len(description.strip()) < 10:
        return {
            "status": "rejected",
            "message": "Please provide more details about the glitch.",
        }

    matches = retrieve_matches(description, platform)
    confidence = calculate_confidence(description, matches)
    category = classify_glitch(description)

    if not matches:
        return {
            "status": "complete",
            "category": category,
            "confidence": confidence,
            "possible_causes": [],
            "recommended_steps": [
                "Provide the exact error message.",
                "Include the game title and platform.",
                "Explain when the problem started.",
                "Describe any recent updates or modifications.",
            ],
            "warning": (
                "There was not enough information to provide "
                "a reliable diagnosis."
            ),
            "retrieved_source_ids": [],
        }

    causes = []
    steps = []

    for result in matches:
        if result["possible_cause"] not in causes:
            causes.append(result["possible_cause"])

        for step in result["steps"]:
            if step not in steps:
                steps.append(step)

    warning = None

    if confidence < 0.6:
        warning = (
            "Confidence is low. Review the suggestions carefully "
            "and provide more details if possible."
        )

    return {
        "status": "complete",
        "category": category,
        "confidence": confidence,
        "possible_causes": causes[:3],
        "recommended_steps": steps[:6],
        "warning": warning,
        "retrieved_source_ids": [
            result["id"] for result in matches
        ],
    }