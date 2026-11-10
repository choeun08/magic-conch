"""무작위성 시험: 1,000회 뽑아 답변별 횟수가 평균 ±20% 안인지 확인"""
from collections import Counter

from answers import ANSWERS
from answers import pick_answer

N = 1000
counts = Counter(pick_answer() for _ in range(N))
avg = N / len(ANSWERS)
for answer in ANSWERS:
    c = counts[answer]
    ok = abs(c - avg) <= avg * 0.2
    print(f"{answer:<20} {c:>4}  {'OK' if ok else 'FAIL'}")
