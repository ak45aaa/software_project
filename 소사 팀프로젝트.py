import os

# ==========================================
# 1. 명령어 처리 함수들 (Built-in Commands)
# ==========================================
def builtin_help(args):
    """도움말 출력"""
    print("--- Python OS Available Commands ---")
    print("help  : Show this help message")
    print("clear : Clear the terminal screen")
    print("echo  : Print text to the screen (e.g., echo hello)")
    print("exit  : Exit the OS")
    print("------------------------------------")

def builtin_clear(args):
    """화면 지우기"""
    # Windows는 'cls', Mac/Linux는 'clear' 명령 실행
    os.system('cls' if os.name == 'nt' else 'clear')

def builtin_echo(args):
    """입력받은 인자 그대로 출력"""
    if not args:
        print("") # 인자가 없으면 빈 줄 출력
    else:
        print(" ".join(args))

# ==========================================
# 2. 명령어 매핑 테이블 (명령어-함수 연결)
# ==========================================
COMMAND_TABLE = {
    "help": builtin_help,
    "clear": builtin_clear,
    "echo": builtin_echo,
}

# ==========================================
# 3. 핵심 파서 및 메인 루프 엔진
# ==========================================
def parse_command(user_input):
    """입력된 문자열을 명령어와 인자 리스트로 분리"""
    tokens = user_input.strip().split()
    if not tokens:
        return None, []
    
    cmd = tokens[0]
    args = tokens[1:]
    return cmd, args

def main_loop():
    """터미널 구동 메인 루프"""
    builtin_clear(None) # 시작할 때 화면 깔끔하게 정리
    print("Welcome to Python OS (v1.0)")
    print("Type 'help' to see available commands.\n")
    
    while True:
        try:
            # 프롬프트 입력 받기
            user_input = input("user@pythonOS:~$ ")
            
            # 아무것도 입력하지 않고 엔터 친 경우 무시
            if not user_input.strip():
                continue
                
            # 문자열 파싱
            cmd, args = parse_command(user_input)
            
            # 종료 명령어는 루프를 빠져나가야 하므로 메인에서 직접 처리
            if cmd == "exit":
                print("Logout. Goodbye!")
                break
            
            # 명령어 실행 및 에러 처리
            if cmd in COMMAND_TABLE:
                COMMAND_TABLE[cmd](args)
            else:
                print(f"pythonOS: {cmd}: command not found")
                
        except KeyboardInterrupt:
            # 사용자가 Ctrl + C를 눌러도 꺼지지 않도록 방어
            print("\nUse 'exit' to log out.")
        except Exception as e:
            print(f"Runtime Error: {e}")

if __name__ == "__main__":
    main_loop()