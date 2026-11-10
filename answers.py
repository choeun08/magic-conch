# 소라고동 답변 목록 - 여기에 문장만 추가하면 바로 반영됨
ANSWERS = [
    "그래.",
    "당연하지.",
    "아니.",
    "절대 안 돼.",
    "지금은 때가 아니야.",
    "다시 물어봐.",
    "그건 네 마음이 알고 있어.",
]

import random


def pick_answer():
    """답변 목록에서 하나를 무작위로 고른다."""
    return random.choice(ANSWERS)
