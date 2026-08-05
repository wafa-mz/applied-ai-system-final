from glitch_retriever import (
    build_diagnosis,
    calculate_confidence,
    classify_glitch,
    load_knowledge_base,
    retrieve_matches,
)


def test_knowledge_base_loads():
    records = load_knowledge_base()

    assert isinstance(records, list)
    assert len(records) >= 7


def test_crashing_issue_is_classified():
    description = (
        "My game crashes every time I launch it "
        "and closes to the desktop."
    )

    category = classify_glitch(description)

    assert category == "crashing"


def test_network_issue_is_classified():
    description = (
        "The multiplayer server keeps disconnecting "
        "and my ping is very high."
    )

    category = classify_glitch(description)

    assert category == "network"


def test_audio_issue_is_classified():
    description = (
        "There is no sound or audio when I start the game."
    )

    category = classify_glitch(description)

    assert category == "audio"


def test_retrieval_returns_matching_record():
    description = (
        "My controller joystick has drift and the input "
        "moves without me touching it."
    )

    matches = retrieve_matches(
        description=description,
        platform="Xbox",
    )

    assert len(matches) > 0
    assert matches[0]["category"] == "controller"
    assert matches[0]["retrieval_score"] > 1


def test_complete_diagnosis_contains_recommendations():
    result = build_diagnosis(
        description=(
            "My game crashes whenever I launch it "
            "and immediately closes."
        ),
        platform="PC",
    )

    assert result["status"] == "complete"
    assert result["category"] == "crashing"
    assert result["confidence"] > 0
    assert len(result["possible_causes"]) > 0
    assert len(result["recommended_steps"]) > 0
    assert len(result["retrieved_source_ids"]) > 0


def test_empty_input_is_rejected():
    result = build_diagnosis(
        description="",
        platform="PC",
    )

    assert result["status"] == "rejected"
    assert "describe" in result["message"].lower()


def test_short_input_is_rejected():
    result = build_diagnosis(
        description="It lags",
        platform="PC",
    )

    assert result["status"] == "rejected"
    assert "more details" in result["message"].lower()


def test_unknown_detailed_issue_returns_limited_guidance():
    result = build_diagnosis(
        description=(
            "A strange symbol appears only after opening "
            "a hidden menu in the game."
        ),
        platform="PC",
    )

    assert result["status"] == "complete"
    assert result["category"] == "unknown"
    assert result["confidence"] == 0.2
    assert result["possible_causes"] == []
    assert len(result["recommended_steps"]) > 0
    assert result["warning"] is not None


def test_confidence_is_between_zero_and_one():
    matches = retrieve_matches(
        description=(
            "The game crashes during launch and closes "
            "to the desktop."
        ),
        platform="PC",
    )

    confidence = calculate_confidence(
        description=(
            "The game crashes during launch and closes "
            "to the desktop."
        ),
        retrieved_results=matches,
    )

    assert 0.0 <= confidence <= 1.0