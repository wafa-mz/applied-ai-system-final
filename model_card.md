# Model Card: Game Glitch Investigator AI

## System Purpose

The Game Glitch Investigator AI helps users describe common video game problems and receive possible causes and safe troubleshooting steps. The system classifies the issue, retrieves matching records from a local troubleshooting knowledge base, calculates a confidence score, and generates a structured diagnosis.

The system is intended for general troubleshooting support only. It does not access the user's device, change settings, delete files, or guarantee that a recommendation will solve the problem.

## Original Project

The original project was **GameGlitch**, created in an earlier module. Its goal was to provide a simple interactive game experience and demonstrate Python logic, user input handling, scoring, and testing.

For this final project, I preserved the original application as `legacy_game.py` and extended the project into an AI-assisted glitch investigation system.

## AI Feature

The main AI feature is retrieval-based troubleshooting. The system reads records from `data/glitch_knowledge.json`, compares the user's description and platform with stored categories and keywords, ranks relevant records, and uses the retrieved information to produce possible causes and recommended steps.

The system also includes confidence scoring, input validation, logging, fallback guidance, and automated reliability tests.

## Limitations and Biases

The system has several limitations:

- It depends on a small, manually created local knowledge base.
- It may not recognize rare, highly technical, game-specific, or newly released issues.
- Keyword matching can miss problems described with unexpected wording.
- Confidence scores are based on retrieval matches and are not guarantees.
- The system may favor common PC and console problems because those issues are better represented in the current data.
- It does not inspect hardware, game files, error codes, system logs, or network conditions directly.
- The recommendations are general and may not fit every game, platform, account, or device.

These limitations mean the system should be treated as a first troubleshooting step, not a replacement for official support or expert technical review.

## Potential Misuse and Prevention

The system could be misused if someone treats its output as guaranteed, performs risky changes without backups, or enters private information such as passwords, account credentials, private server addresses, or personal data.

To reduce these risks, the application:

- Displays a warning to back up important save data.
- Tells users not to enter sensitive information.
- Provides general troubleshooting steps instead of destructive commands.
- Does not access or modify the user's device.
- Rejects empty and overly short descriptions.
- Displays a warning when confidence is low.
- Shows which knowledge-base records were used.
- Logs investigations for review.

Future versions could add stronger filtering for sensitive data and clearer escalation instructions for official customer support.

## Reliability Testing

The system was evaluated with automated tests using `pytest`.

The new reliability suite included 10 tests covering:

- Knowledge-base loading
- Crashing classification
- Network classification
- Audio classification
- Controller retrieval
- Complete diagnosis generation
- Empty-input rejection
- Short-input rejection
- Unknown-issue fallback behavior
- Confidence score boundaries

All 10 new tests passed. The complete repository test suite contained 23 tests, and all 23 passed.

The full test output is saved in `test_results.txt`.

## What Surprised Me During Testing

I was surprised that simple wording changes could affect retrieval scores and classification. Detailed descriptions with clear keywords produced strong matches and high confidence, while unusual or vague descriptions produced lower confidence and limited guidance.

Testing also showed why guardrails are important. Without validation, empty or extremely short descriptions could produce weak or misleading results. Adding rejection rules made the system safer and more consistent.

## Collaboration With AI

I used AI as a development assistant while building this project. It helped me plan the folder structure, design the retrieval workflow, create a Mermaid architecture diagram, draft test cases, and improve the Streamlit interface.

One helpful AI suggestion was to separate the troubleshooting knowledge base from the application code. Moving the records into `data/glitch_knowledge.json` made the project easier to maintain, test, and expand.

One flawed AI suggestion occurred when a file-renaming command and another command were accidentally placed on the same line:

```bash
mv ai_coach.py glitch_retriever.py ls
```

This failed because `mv` interpreted `ls` as another destination argument. I corrected it by running the commands separately:

```bash
mv ai_coach.py glitch_retriever.py
ls
```

This taught me that AI-generated commands must be reviewed carefully before execution.

## Responsible Use

Users should:

- Back up save data before changing game or system settings.
- Avoid entering passwords or private account information.
- Review recommendations before following them.
- Contact official game, console, or hardware support for serious or unresolved issues.
- Treat confidence scores as guidance rather than certainty.

## Future Improvements

Future improvements could include:

- More troubleshooting records and game-specific sources
- Error-code lookup
- Multiple knowledge sources
- Better semantic matching instead of basic keyword matching
- Stronger privacy filtering
- Human evaluation records
- A formal evaluation script
- Links to official support documentation