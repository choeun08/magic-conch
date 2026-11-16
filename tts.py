import queue
import threading

import pyttsx3

_queue = queue.Queue()  # 읽을 답변을 넣어 두는 줄
_current = {"started": None}  # 지금 읽는 답변의 "말하기 시작" 신호


def _on_start(name):
    """엔진이 실제로 말하기 시작하면 신호를 켠다."""
    if _current["started"] is not None:
        _current["started"].set()


def _worker():
    """프로그램이 켜질 때 음성 엔진을 미리 한 번만 준비해 두고, 답변이 들어오면 바로 읽는다."""
    try:
        import comtypes  # 윈도우: 새 스레드에서 음성 엔진을 쓰기 위한 준비
        comtypes.CoInitialize()
    except Exception:
        pass

    engine = pyttsx3.init()
    engine.setProperty("rate", 185)
    engine.setProperty("volume", 1.0)
    engine.connect("started-utterance", _on_start)

    for voice in engine.getProperty("voices"):
        voice_info = (voice.name + " " + voice.id).lower()
        if "korean" in voice_info or "ko-kr" in voice_info or "한국" in voice_info:
            engine.setProperty("voice", voice.id)
            break

    while True:
        text, started = _queue.get()
        _current["started"] = started
        engine.say(text)
        engine.runAndWait()


# 프로그램 시작과 동시에 엔진 준비 (첫 답변부터 바로 읽을 수 있게)
threading.Thread(target=_worker, daemon=True).start()


def speak(answer, started=None):
    """답변을 읽어 달라고 줄에 넣는다. 말하기 시작하면 started 신호가 켜진다."""
    while not _queue.empty():  # 아직 못 읽은 예전 답변은 버리고 최신 답변만
        try:
            _queue.get_nowait()
        except queue.Empty:
            break
    _queue.put((answer, started))
