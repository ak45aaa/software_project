# software_project

소사 팀플

## StudentOS AI Assistant

이 프로젝트의 AI Assistant 코드는 `chatbot/` 폴더 안에 있습니다.

이 AI Assistant는 일반적인 ChatGPT 클론이 아니라, 사용자의 자연어 입력을 StudentOS 터미널에서 사용할 수 있는 구조화된 명령으로 바꾸는 역할을 합니다.

예시:

```text
사용자 입력: create a folder called homework
AI 출력: {"action": "create_folder", "path": "homework"}
```

## 실행 방법

먼저 Ollama를 실행하고 모델을 준비해야 합니다.

```powershell
ollama pull llama3.2:3b
```

CLI 버전 실행:

```powershell
python -m chatbot.main
```

Tkinter GUI 버전 실행:

```powershell
python -m chatbot.gui
```

## 사용 기술

이 assistant는 OpenAI API를 사용하지 않고, Ollama를 로컬에서 사용합니다.

기본 설정:

- 모델: `llama3.2:3b`
- API 주소: `http://localhost:11434/api/generate`

필요하면 환경 변수로 모델명과 API 주소를 바꿀 수 있습니다.

```powershell
$env:OLLAMA_MODEL = "llama3.2:3b"
$env:OLLAMA_URL = "http://localhost:11434/api/generate"
```

## 명령 구조

AI는 다음과 같은 JSON 형식의 명령을 반환합니다.

```json
{"action": "create_folder", "path": "homework"}
```

현재 지원하는 action:

- `create_file`
- `create_folder`
- `delete_file`
- `delete_folder`
- `list_files`
- `chat`

## 안전성

AI가 만든 문자열을 그대로 쉘에서 실행하지 않습니다.

- `exec()` 사용 안 함
- 임의의 쉘 명령 실행 안 함
- 허용된 action만 실행
- 절대경로 차단
- 작업 폴더 밖으로 나가는 경로 차단

## 파일 구조

```text
chatbot/
├── __init__.py
├── README.md
├── chatbot.py
├── command_executor.py
├── command_parser.py
├── gui.py
└── main.py
```

주요 파일 역할:

- `chatbot.py`: Ollama 호출 및 자연어를 명령으로 변환하는 흐름 담당
- `command_parser.py`: AI 응답에서 JSON 추출 및 명령 검증
- `command_executor.py`: 검증된 명령을 안전하게 실행
- `main.py`: CLI 실행 파일
- `gui.py`: Tkinter GUI 실행 파일

## 한글 Windows 사용자 이름 관련 Ollama 오류

Windows 사용자 이름에 한글이 포함된 경우 Ollama가 모델 경로를 제대로 읽지 못할 수 있습니다.

예시 오류:

```text
C:\Users\����\.ollama\models\...
llama_model_loader: failed to load model
```

이 경우 모델 저장 위치를 영어 경로로 바꿉니다.

```powershell
mkdir C:\OllamaModels
setx OLLAMA_MODELS C:\OllamaModels
ollama pull llama3.2:3b
```

이미 모델을 다운로드했다면 기존 `.ollama\models` 안의 `blobs`, `manifests` 폴더를 `C:\OllamaModels`로 복사해도 됩니다.
