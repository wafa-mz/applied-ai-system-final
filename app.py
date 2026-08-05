from datetime import datetime
import json
from pathlib import Path

import streamlit as st

from glitch_retriever import build_diagnosis


LOG_PATH = Path(__file__).resolve().parent / "logs" / "investigations.jsonl"

SUPPORTED_PLATFORMS = [
    "PC",
    "PlayStation",
    "Xbox",
    "Nintendo Switch",
]


def save_log(platform, description, result):
    """Save a structured record of each investigation."""
    LOG_PATH.parent.mkdir(exist_ok=True)

    log_entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "platform": platform,
        "description": description,
        "status": result.get("status"),
        "category": result.get("category"),
        "confidence": result.get("confidence"),
        "retrieved_source_ids": result.get(
            "retrieved_source_ids",
            [],
        ),
    }

    with open(LOG_PATH, "a", encoding="utf-8") as file:
        file.write(json.dumps(log_entry) + "\n")


st.set_page_config(
    page_title="Game Glitch Investigator AI",
    page_icon="🎮",
    layout="centered",
)

st.title("🎮 Game Glitch Investigator AI")

st.write(
    "Describe a video game problem and the system will retrieve "
    "matching troubleshooting information, classify the issue, "
    "and recommend safe next steps."
)

st.info(
    "The recommendations are general troubleshooting guidance. "
    "Back up important save data before making system changes."
)

platform = st.selectbox(
    "Gaming platform",
    SUPPORTED_PLATFORMS,
)

description = st.text_area(
    "Describe the glitch",
    placeholder=(
        "Example: My game crashes every time I launch it "
        "and closes back to the desktop."
    ),
    height=140,
    max_chars=2000,
)

investigate = st.button(
    "Investigate Glitch",
    type="primary",
)

if investigate:
    result = build_diagnosis(
        description=description,
        platform=platform,
    )

    if result["status"] == "rejected":
        st.error(result["message"])

    else:
        save_log(
            platform=platform,
            description=description,
            result=result,
        )

        st.divider()
        st.subheader("Investigation Report")

        category = result["category"].replace("_", " ").title()
        confidence = result["confidence"]

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Issue category", category)

        with col2:
            st.metric(
                "Confidence",
                f"{confidence:.0%}",
            )

        if result["possible_causes"]:
            st.subheader("Possible causes")

            for cause in result["possible_causes"]:
                st.write(f"- {cause}")

        st.subheader("Recommended steps")

        for number, step in enumerate(
            result["recommended_steps"],
            start=1,
        ):
            st.write(f"{number}. {step}")

        if result["warning"]:
            st.warning(result["warning"])

        with st.expander("Retrieval details"):
            source_ids = result["retrieved_source_ids"]

            if source_ids:
                st.write(
                    "Knowledge-base records used:",
                    source_ids,
                )
            else:
                st.write(
                    "No matching knowledge-base record was found."
                )

            st.write(
                "The diagnosis and recommendations above were "
                "generated from the retrieved records."
            )

st.divider()

with st.expander("Privacy and safety"):
    st.write(
        "Do not enter passwords, account credentials, private "
        "server addresses, or other sensitive information."
    )
    st.write(
        "The system does not delete files, alter settings, or "
        "access the gaming device directly."
    )