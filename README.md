# StudentOS AI Assistant

StudentOS AI Assistant는 Python으로 구현한 **가상 터미널 기반 미니 운영체제 프로젝트**입니다.  
사용자는 GUI 터미널에 직접 명령어를 입력할 수도 있고, 오른쪽 AI Assistant 창에 자연어로 명령을 입력하여 파일/폴더 작업을 수행할 수도 있습니다.

이 프로젝트는 실제 컴퓨터의 파일 시스템을 직접 조작하지 않고, Python 객체로 구현한 **가상 파일 시스템** 안에서 안전하게 동작합니다.

---

## 1. 프로젝트 개요

본 프로젝트의 목표는 운영체제의 기본적인 터미널 동작을 직접 구현하고, 여기에 AI 자연어 명령 처리 기능을 결합하는 것입니다.

사용자는 다음 두 가지 방식으로 StudentOS를 사용할 수 있습니다.

1. 터미널 명령어 직접 입력  
   예: `mkdir test`, `touch memo.txt`, `ls`

2. AI 자연어 명령 입력  
   예: `test 폴더 만들어줘`, `memo.txt 파일 내용을 보여줘`

AI가 자연어를 JSON 형태의 명령으로 변환하면, 실행기가 이를 해석하여 가상 파일 시스템에 명령을 적용합니다.

---

## 2. 주요 기능

### 2.1 GUI 가상 터미널

Tkinter를 이용하여 터미널 형태의 GUI를 구현했습니다.

지원 기능:

- 터미널 프롬프트 출력
- 명령어 입력 및 실행
- 실행 결과 출력
- 현재 디렉토리 표시
- `clear` 명령으로 화면 초기화

예시:

```bash
user@pythonOS:~$ mkdir project
user@pythonOS:~$ cd project
user@pythonOS:/project$ touch memo.txt
user@pythonOS:/project$ ls
memo.txt
```

---

### 2.2 가상 파일 시스템

실제 컴퓨터 파일을 건드리지 않고, Python 클래스를 이용하여 파일과 디렉토리 구조를 구현했습니다.

구성 요소:

- `File`: 파일 객체
- `Directory`: 디렉토리 객체
- `FileSystem`: 전체 파일 시스템 관리 객체

예시 구조:

```text
/
├── project
│   └── memo.txt
└── homework
```

지원 기능:

- 현재 위치 확인
- 디렉토리 이동
- 파일 생성
- 폴더 생성
- 파일 삭제
- 폴더 삭제
- 파일 목록 출력
- 파일 내용 읽기
- 파일 내용 쓰기

---

### 2.3 AI 자연어 명령 처리

Ollama 로컬 LLM을 이용하여 자연어 입력을 StudentOS에서 실행 가능한 JSON 명령으로 변환합니다.

예시:

사용자 입력:

```text
notes.txt 파일 만들어줘
```

AI 변환 결과:

```json
{"action": "create_file", "path": "notes.txt"}
```

실행되는 터미널 명령:

```bash
touch notes.txt
```

---

## 3. 지원 명령어

### 3.1 직접 터미널 명령어

| 명령어 | 설명 |
|---|---|
| `help` | 사용 가능한 명령어 출력 |
| `clear` | 터미널 화면 지우기 |
| `pwd` | 현재 디렉토리 출력 |
| `ls [path]` | 파일/폴더 목록 출력 |
| `cd <path>` | 디렉토리 이동 |
| `mkdir <path>` | 폴더 생성 |
| `touch <path>` | 파일 생성 |
| `cat <path>` | 파일 내용 출력 |
| `write <file> <content>` | 파일에 내용 쓰기 |
| `echo <text>` | 입력한 텍스트 출력 |
| `rm <path>` | 파일 삭제 |
| `rmdir <path>` | 빈 폴더 삭제 |
| `exit` | 프로그램 종료 |

---

### 3.2 AI 지원 명령

| Action | 설명 | 예시 |
|---|---|---|
| `create_file` | 파일 생성 | `notes.txt 파일 만들어줘` |
| `create_folder` | 폴더 생성 | `homework 폴더 만들어줘` |
| `delete_file` | 파일 삭제 | `notes.txt 삭제해줘` |
| `delete_folder` | 폴더 삭제 | `homework 폴더 삭제해줘` |
| `list_files` | 파일 목록 보기 | `현재 폴더에 뭐 있어?` |
| `read_file` | 파일 내용 읽기 | `notes.txt 내용 보여줘` |
| `write_file` | 파일에 내용 쓰기 | `notes.txt에 hello 써줘` |
| `chat` | 일반 응답 | 지원하지 않는 요청에 대한 답변 |

---

## 4. 프로젝트 구조

```text
chatbot/
├── __init__.py
├── main.py
├── gui.py
├── chatbot.py
├── command_parser.py
├── virtual_filesystem.py
└── virtual_executor.py
```

각 파일의 역할은 다음과 같습니다.

### `main.py`

프로그램 실행 시작점입니다.

```python
from .gui import main

if __name__ == "__main__":
    main()
```

---

### `gui.py`

Tkinter 기반 GUI를 담당합니다.

역할:

- 왼쪽 터미널 화면 구성
- 오른쪽 AI Assistant 화면 구성
- 사용자 입력 처리
- 터미널 명령 실행 연결
- AI 자연어 명령 실행 연결

---

### `chatbot.py`

Ollama API와 통신하여 자연어 입력을 JSON 명령으로 변환합니다.

역할:

- 시스템 프롬프트 관리
- Ollama 서버에 요청 전송
- AI 응답 수신
- 명령 파서로 결과 전달

---

### `command_parser.py`

AI가 만든 JSON 명령을 검증하고 정규화합니다.

역할:

- JSON 객체 추출
- 허용된 action만 통과
- 잘못된 명령을 chat 응답으로 변환
- 간단한 영어 명령은 rule-based 방식으로 처리

---

### `virtual_filesystem.py`

가상 파일 시스템을 구현합니다.

역할:

- 파일 객체 관리
- 디렉토리 객체 관리
- 경로 해석
- `cd`, `ls`, `mkdir`, `touch`, `cat`, `rm`, `rmdir` 등의 핵심 기능 제공

---

### `virtual_executor.py`

터미널 명령어와 AI JSON 명령을 실제 파일 시스템 기능에 연결합니다.

역할:

- `mkdir test` 같은 직접 명령어 실행
- `{"action": "create_folder", "path": "test"}` 같은 AI 명령 실행
- AI 명령을 터미널 명령 형태로 변환하여 출력

---

## 5. 실행 방법

### 5.1 Ollama 설치 및 모델 준비

먼저 Ollama를 실행하고 모델을 다운로드합니다.

```bash
ollama pull llama3.2:3b
```

Ollama 서버가 실행 중이어야 AI Assistant 기능을 사용할 수 있습니다.

---

### 5.2 프로그램 실행

프로젝트 최상위 폴더에서 다음 명령어를 실행합니다.

```bash
python -m chatbot.main
```

또는 `gui.py`를 직접 실행할 수도 있습니다.

```bash
python chatbot/gui.py
```

---

## 6. 실행 흐름

### 6.1 직접 터미널 명령 실행 흐름

```text
사용자 명령 입력
→ gui.py
→ virtual_executor.py
→ virtual_filesystem.py
→ 실행 결과 GUI 출력
```

예시:

```text
mkdir test
→ execute_terminal_command()
→ FileSystem.mkdir("test")
→ test 폴더 생성
```

---

### 6.2 AI 자연어 명령 실행 흐름

```text
사용자 자연어 입력
→ gui.py
→ chatbot.py
→ command_parser.py
→ virtual_executor.py
→ virtual_filesystem.py
→ 실행 결과 GUI 출력
```

예시:

```text
"test 폴더 만들어줘"
→ Ollama
→ {"action": "create_folder", "path": "test"}
→ execute_ai_command()
→ FileSystem.mkdir("test")
```

---

## 7. 안전성

이 프로젝트는 실제 운영체제의 파일을 직접 조작하지 않습니다.

안전성을 위해 다음과 같은 구조를 사용했습니다.

- 실제 `os.remove`, `shutil.rmtree` 등을 사용하지 않음
- Python 객체 기반 가상 파일 시스템 사용
- AI 응답을 바로 실행하지 않고 JSON 명령으로 검증
- 허용된 action만 실행
- 지원하지 않는 명령은 실행하지 않고 안내 메시지 출력

---

## 8. 시연 예시

### 8.1 직접 터미널 명령 시연

```bash
help
mkdir project
cd project
touch memo.txt
write memo.txt hello StudentOS
cat memo.txt
pwd
ls
```

예상 결과:

```text
hello StudentOS
/project
memo.txt
```

---

### 8.2 AI Assistant 시연

오른쪽 AI Assistant 입력창에 다음과 같이 입력합니다.

```text
notes 폴더 만들어줘
```

예상 실행:

```json
{"action": "create_folder", "path": "notes"}
```

터미널 출력:

```bash
$ mkdir notes
```

다음 입력:

```text
memo.txt 내용을 보여줘
```

예상 실행:

```json
{"action": "read_file", "path": "memo.txt"}
```

터미널 출력:

```bash
$ cat memo.txt
hello StudentOS
```

---

## 9. 프로젝트 특징

이 프로젝트의 가장 큰 특징은 단순한 명령어 처리 프로그램이 아니라, 다음 세 가지를 통합했다는 점입니다.

1. GUI 기반 가상 터미널
2. Python 객체 기반 가상 파일 시스템
3. AI 자연어 명령 처리

따라서 사용자는 일반 터미널처럼 명령어를 직접 입력할 수도 있고, 자연어로 파일 작업을 요청할 수도 있습니다.

---

## 10. 향후 개선 방향

추가로 구현하면 좋은 기능은 다음과 같습니다.

- AI를 통한 `cd`, `pwd` 명령 지원
- 파일 복사 명령 `cp`
- 파일 이동 및 이름 변경 명령 `mv`
- 폴더 재귀 삭제 `rm -r`
- 파일 내용 추가 쓰기 `append`
- 사용자 권한 기능
- 가짜 프로세스 관리 기능
- 명령어 히스토리 기능
- 더 정교한 한국어 자연어 명령 처리

---

## 11. 결론

StudentOS AI Assistant는 운영체제의 기본 구조를 학습하기 위해 만든 가상 터미널 프로젝트입니다.  
파일과 디렉토리를 객체로 직접 구현하고, GUI 터미널과 AI 자연어 명령 기능을 연결하여 사용자가 더 직관적으로 명령을 실행할 수 있도록 설계했습니다.

이 프로젝트를 통해 명령어 파싱, 파일 시스템 구조, GUI 이벤트 처리, AI 명령 변환, 실행기 설계 등 운영체제와 소프트웨어 구조에 관련된 다양한 개념을 종합적으로 구현했습니다.
