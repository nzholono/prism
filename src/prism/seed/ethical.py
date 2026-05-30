"""Seed data: the four ethical frameworks.

Idempotent — uses INSERT OR IGNORE on the unique `slug` column.
"""

from __future__ import annotations

import json
import sqlite3

FRAMEWORKS = [
    {
        "slug": "utilitarian",
        "name": "Utilitarian",
        "description_md": (
            "Founded by Jeremy Bentham and refined by John Stuart Mill, utilitarianism "
            "holds that the right action is the one that produces the greatest overall "
            "wellbeing for everyone affected. It evaluates choices by their consequences."
        ),
        "key_questions": [
            "Who is affected by each option, including people I am not in direct contact with?",
            "What is the net change in wellbeing under each option?",
            "Am I weighting some people's wellbeing more than others without justification?",
            "What are the longer-term consequences, not just the immediate ones?",
        ],
    },
    {
        "slug": "deontological",
        "name": "Deontological",
        "description_md": (
            "Rooted in Kant's work, deontology says some actions are right or wrong "
            "regardless of their outcomes. It focuses on duties, rights, and rules that "
            "would hold even if breaking them produced a better result."
        ),
        "key_questions": [
            "If everyone in my position took this option, would I want to live in that world?",
            "Am I treating anyone here merely as a means to an end?",
            "What duties do I have here, and to whom?",
            "Whose rights are at stake?",
        ],
    },
    {
        "slug": "virtue",
        "name": "Virtue Ethics",
        "description_md": (
            "Traced to Aristotle, virtue ethics asks not 'what should I do' but 'who am "
            "I becoming'. The right action is the one a person of good character would "
            "take — someone honest, courageous, fair, and prudent."
        ),
        "key_questions": [
            "Which option reflects the character I want to have?",
            "Which virtues does this choice exercise — and which does it neglect?",
            "Would I respect this choice if I saw someone else make it?",
            "Am I being honest with myself about my real motives?",
        ],
    },
    {
        "slug": "care",
        "name": "Care Ethics",
        "description_md": (
            "Developed by Carol Gilligan and Nel Noddings, care ethics centers the "
            "concrete relationships and needs of specific people. It treats moral "
            "reasoning as inseparable from the texture of our connections to others."
        ),
        "key_questions": [
            "Whose voice is missing from my reasoning?",
            "Which option best preserves the relationships I value?",
            "Whose needs am I attending to, and whose am I overlooking?",
            "How will the people closest to this feel — not just be affected, but feel?",
        ],
    },
]


def seed(conn: sqlite3.Connection) -> None:
    for fw in FRAMEWORKS:
        conn.execute(
            "INSERT OR IGNORE INTO ethical_frameworks "
            "(slug, name, description_md, key_questions) VALUES (?, ?, ?, ?)",
            (fw["slug"], fw["name"], fw["description_md"], json.dumps(fw["key_questions"])),
        )
    conn.commit()
