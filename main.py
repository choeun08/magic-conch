"""마법의 소라고동 - 화면 설계(2.1) 버전

① 시작 화면 → ② 질문 쓰고 줄 클릭 → ③ 답변 팝업 → 다시하기(②로)
"""
import tkinter as tk

from answers import pick_answer

# ---------------- 화면 설정 ----------------
WIDTH, HEIGHT = 420, 600
BG = "#f6f1fb"            # 배경색(연보라)
SHELL = "#b39ddb"         # 소라 껍데기 색(보라)
SHELL_LIGHT = "#e3d7f7"   # 껍데기 밝은 부분
SHELL_LINE = "#5e35b1"    # 테두리(진보라)
BAND = "#7e57c2"          # 나선 줄무늬
INSIDE = "#f3c6e4"        # 입구 안쪽(분홍빛 보라)
INSIDE_DEEP = "#d48ac0"   # 입구 깊은 곳
STRING_COLOR = "#4a2c7a"  # 줄 색
FONT = "맑은 고딕"

CONCH_X = 210                 # 소라고동 가운데 x 위치
STRING_TOP = 250              # 줄이 시작하는 높이(소라 아래 뾰족한 끝)
STRING_LEN = 40               # 평소 줄 길이
PULL_LEN = 120                # 다 당겼을 때 줄 길이
STEPS = 15                    # 당기기(또는 돌아오기) 단계 수
STEP_MS = 50                  # 단계당 시간 -> 당기기+돌아오기 약 1.5초

# 소라 모양 좌표 (가운데 x 기준으로 얼마나 떨어졌는지, y는 위에서부터)
BODY = [(0, 40), (18, 62), (42, 84), (68, 108), (80, 140), (72, 175),
        (48, 205), (18, 230), (4, 250), (-6, 230), (-34, 205), (-62, 172),
        (-74, 140), (-62, 108), (-38, 84), (-16, 62)]
BANDS = [[(-16, 62), (0, 70), (18, 62)],
         [(-38, 84), (2, 98), (42, 84)],
         [(-62, 108), (4, 126), (68, 108)]]
KNOBS = [-48, -18, 14, 46]    # 어깨에 난 뿔(돌기)의 x 위치
APERTURE = [(10, 128), (48, 138), (64, 166), (54, 198), (28, 224),
            (10, 204), (4, 166)]
APERTURE_DEEP = [(16, 150), (40, 158), (48, 178), (38, 200), (22, 206),
                 (14, 180)]
STRING_TIP = 4                # 줄이 달린 아래 끝 x


def shift(points, cx):
    """기준 좌표를 실제 화면 좌표 목록으로 바꾼다."""
    return [v for x, y in points for v in (cx + x, y)]


def draw_conch(canvas, cx, tag):
    """코드로 보라색 소라고동을 그린다. (나중에 이미지로 바꿀 수 있음)"""
    canvas.create_polygon(shift(BODY, cx), smooth=True, fill=SHELL,
                          outline=SHELL_LINE, width=3, tags=tag)
    canvas.create_line(shift([(-56, 120), (-66, 145), (-58, 172), (-36, 200)], cx),
                       smooth=True, fill=SHELL_LIGHT, width=6,
                       capstyle="round", tags=tag)   # 반짝이는 부분
    for band in BANDS:                                # 나선 줄무늬
        canvas.create_line(shift(band, cx), smooth=True, fill=BAND,
                           width=3, tags=tag)
    for kx in KNOBS:                                  # 어깨 돌기
        canvas.create_polygon(shift([(kx - 7, 118), (kx, 102), (kx + 7, 118)], cx),
                              fill=SHELL, outline=SHELL_LINE, width=2, tags=tag)
    canvas.create_polygon(shift(APERTURE, cx), smooth=True, fill=INSIDE,
                          outline=SHELL_LINE, width=2, tags=tag)
    canvas.create_polygon(shift(APERTURE_DEEP, cx), smooth=True,
                          fill=INSIDE_DEEP, outline="", tags=tag)


class ConchApp:
    """소라고동 프로그램 전체를 관리한다."""

    def __init__(self, root):
        self.root = root
        root.title("마법의 소라고동")
        root.geometry(f"{WIDTH}x{HEIGHT}")
        root.configure(bg=BG)
        root.resizable(False, False)

        self.animating = False  # 애니메이션 중 중복 클릭 방지
        self.popup = None

        self.start_frame = self.build_start_screen()
        self.question_frame = self.build_question_screen()
        self.show(self.start_frame)

    # ---------------- 화면 만들기 ----------------
    def build_start_screen(self):
        """① 시작 화면: 제목 + 소라고동 그림."""
        frame = tk.Frame(self.root, bg=BG)
        tk.Label(frame, text="마법의 소라고동", font=(FONT, 22, "bold"),
                 bg=BG).pack(pady=(24, 0))
        canvas = tk.Canvas(frame, width=WIDTH, height=290, bg=BG,
                           highlightthickness=0, cursor="hand2")
        canvas.pack()
        draw_conch(canvas, CONCH_X, "conch")
        canvas.tag_bind("conch", "<Button-1>", lambda e: self.go_question())
        tk.Label(frame, text="소라고동을 눌러서 시작해 봐", font=(FONT, 12),
                 fg="#6a5a8a", bg=BG).pack(pady=10)
        return frame

    def build_question_screen(self):
        """② 질문 화면: 소라고동 + 줄 + 질문 입력창."""
        frame = tk.Frame(self.root, bg=BG)
        tk.Label(frame, text="마법의 소라고동", font=(FONT, 22, "bold"),
                 bg=BG).pack(pady=(24, 0))

        self.canvas = tk.Canvas(frame, width=WIDTH, height=420, bg=BG,
                                highlightthickness=0)
        self.canvas.pack()
        draw_conch(self.canvas, CONCH_X, "conch")
        bottom = STRING_TOP + STRING_LEN
        self.string_line = self.canvas.create_line(
            CONCH_X + STRING_TIP, STRING_TOP, CONCH_X + STRING_TIP, bottom,
            fill=STRING_COLOR, width=4, tags="string")
        self.handle = self.canvas.create_oval(
            CONCH_X + STRING_TIP - 12, bottom, CONCH_X + STRING_TIP + 12, bottom + 24,
            fill=STRING_COLOR, outline="", tags="string")
        self.canvas.tag_bind("string", "<Button-1>", lambda e: self.pull())
        self.canvas.tag_bind("string", "<Enter>",
                             lambda e: self.canvas.config(cursor="hand2"))
        self.canvas.tag_bind("string", "<Leave>",
                             lambda e: self.canvas.config(cursor=""))

        row = tk.Frame(frame, bg=BG)
        row.pack(pady=5)
        tk.Label(row, text="질문:", font=(FONT, 12), bg=BG).pack(side="left")
        self.entry = tk.Entry(row, width=28, font=(FONT, 12))
        self.entry.pack(side="left", padx=5)
        self.entry.bind("<Return>", lambda e: self.pull())

        self.message = tk.Label(frame, text="질문을 쓰고 줄을 클릭해 봐",
                                font=(FONT, 11), fg="#6a5a8a", bg=BG)
        self.message.pack(pady=8)
        return frame

    # ---------------- 화면 전환 ----------------
    def show(self, frame):
        """보여줄 화면만 남기고 나머지는 숨긴다."""
        for f in (self.start_frame, self.question_frame):
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def go_question(self):
        """① → ② 질문 화면으로 이동한다."""
        self.show(self.question_frame)
        self.entry.focus_set()

    # ---------------- 줄 당기기 ----------------
    def pull(self):
        """줄을 클릭하면: 질문이 있으면 애니메이션, 없으면 안내."""
        if self.animating:
            return
        if not self.entry.get().strip():
            self.message.config(text="질문을 먼저 입력해 줘.", fg="#c0392b")
            return
        self.message.config(text="소라고동이 생각하는 중...", fg="#6a5a8a")
        self.animating = True
        self.animate(0)

    def set_string_length(self, length):
        """줄 길이를 바꿔서 다시 그린다."""
        bottom = STRING_TOP + length
        x = CONCH_X + STRING_TIP
        self.canvas.coords(self.string_line, x, STRING_TOP, x, bottom)
        self.canvas.coords(self.handle, x - 12, bottom, x + 12, bottom + 24)

    def animate(self, step):
        """줄이 저절로 늘어났다가 돌아온 뒤 답변 팝업을 띄운다."""
        if step <= STEPS:                       # 늘어나기
            progress = step / STEPS
        elif step <= STEPS * 2:                 # 돌아오기
            progress = (STEPS * 2 - step) / STEPS
        else:
            self.show_answer()
            return
        self.set_string_length(STRING_LEN + (PULL_LEN - STRING_LEN) * progress)
        self.root.after(STEP_MS, self.animate, step + 1)

    # ---------------- ③ 답변 팝업 ----------------
    def show_answer(self):
        """무작위 답변을 팝업창으로 보여준다."""
        popup = tk.Toplevel(self.root)
        popup.title("소라고동의 대답")
        popup.configure(bg=BG)
        popup.resizable(False, False)
        popup.transient(self.root)
        x = self.root.winfo_rootx() + 40
        y = self.root.winfo_rooty() + 150
        popup.geometry(f"340x200+{x}+{y}")

        tk.Label(popup, text="소라고동의 대답", font=(FONT, 11),
                 fg="#6a5a8a", bg=BG).pack(pady=(20, 5))
        self.answer_label = tk.Label(popup, text=pick_answer(),
                                     font=(FONT, 20, "bold"), bg=BG,
                                     wraplength=300)
        self.answer_label.pack(pady=10)
        tk.Button(popup, text="다시하기", font=(FONT, 11), width=10,
                  command=self.close_answer).pack(pady=10)
        popup.protocol("WM_DELETE_WINDOW", self.close_answer)
        popup.grab_set()  # 팝업이 떠 있는 동안 뒤 화면은 못 누르게
        self.popup = popup

    def close_answer(self):
        """다시하기: 팝업을 닫고 ② 질문 화면으로 돌아간다."""
        if self.popup is not None:
            self.popup.grab_release()
            self.popup.destroy()
            self.popup = None
        self.entry.delete(0, "end")
        self.message.config(text="질문을 쓰고 줄을 클릭해 봐", fg="#6a5a8a")
        self.animating = False
        self.entry.focus_set()


if __name__ == "__main__":
    window = tk.Tk()
    ConchApp(window)
    window.mainloop()
