import tkinter as tk

window = tk.Tk()
window.title("My Virtual Terminal")
window.geometry("700x450")
window.configure(bg="black")

# 1. text 창
terminal = tk.Text(
    window, bg="black", fg="#CCCCCC", insertbackground="white",
    font=("Courier New", 13), borderwidth=0,
    blockcursor=True, highlightthickness=0
)
terminal.pack(fill="both", expand=True, padx=5, pady=5)
terminal.focus()

# 프롬프트 고정 글자
PROMPT = "guest@computer ~ % "

# 프로그램 시작 시 첫 프롬프트 띄우기
terminal.insert("end", PROMPT)

def run_command(event):
    # 현재 줄에 적힌 글자를 통째로 가져옴
    current_line = terminal.get("insert linestart", "end-1c")
    
    # 프롬프트 글자 수만큼 잘라내서 순수 명령어만 추출
    if current_line.startswith(PROMPT):
        command = current_line[len(PROMPT):].strip()
    else:
        command = ""

    # 엔터 쳤으니 다음 줄로 이동
    terminal.insert("end", "\n")
    
    # 명령어 반응 (테스트용)
    if command == "help":
        terminal.insert("end", "사용 가능한 명령어: help, clear, hello\n")
    elif command == "hello":
        terminal.insert("end", "안녕하세요! 가상 터미널입니다.\n")
    elif command == "clear":
        terminal.delete("1.0", "end")
    elif command == "":
        pass
    else:
        terminal.insert("end", "zsh: command not found: " + command + "\n")

    # 명령어가 끝나면 새 프롬프트를 다시 띄움
    terminal.insert("end", PROMPT)
    terminal.see("end") # 화면 맨 아래로 스크롤
    
    return "break" # 엔터키를 눌렀을 때 기본적으로 줄바꿈이 두 번 일어나는 것 방지

# 엔터키 연결
terminal.bind("<Return>", run_command)

window.mainloop()
