# StudentOS AI Assistant

이 패키지는 사용자의 자연어 입력을 StudentOS에서 사용할 수 있는 구조화된 명령으로 변환합니다.

전체 흐름:

```text
사용자 입력 -> 로컬 Ollama 모델 -> JSON 명령 -> 안전한 실행기
```

예시:

```json
{"action": "create_folder", "path": "homework"}
```

## 파일 설명

- `chatbot.py`: Ollama API 호출과 `parse_command()` 흐름 담당
- `command_parser.py`: JSON 추출, 정규화, 간단한 규칙 기반 파싱 담당
- `command_executor.py`: 임의 쉘 실행 없이 안전한 파일/폴더 명령 실행
- `main.py`: CLI 실행 시작점
- `gui.py`: Tkinter GUI 실행 시작점

## 실행 방법

먼저 Ollama를 실행하고 모델을 다운로드합니다.

```powershell
ollama pull llama3.2:3b
```

그 다음 아래 명령 중 하나를 실행합니다.

```powershell
python -m chatbot.main
python -m chatbot.gui
```

## 지원하는 명령

현재 지원하는 action은 다음과 같습니다.

```text
create_file
create_folder
delete_file
delete_folder
list_files
chat
```

예시 JSON:

```json
{"action": "create_file", "path": "notes.txt"}
```

## 안전성

이 코드는 AI가 만든 명령어를 그대로 실행하지 않습니다.

- `exec()` 사용 안 함
- 임의 쉘 명령 실행 안 함
- 허용된 action만 실행
- 절대경로 차단
- 작업 폴더 밖으로 나가는 경로 차단

## 한글 Windows 사용자 이름 관련 Ollama 설정

Windows 사용자 이름에 한글이 포함되어 있으면 Ollama가 모델 경로를 제대로 읽지 못할 수 있습니다.

오류 예시:

```text
C:\Users\����\.ollama\...
llama_model_loader: failed to load model
```

이 경우 모델 저장 위치를 영어 경로로 옮깁니다.

```powershell
mkdir C:\OllamaModels
setx OLLAMA_MODELS C:\OllamaModels
```

그 다음 Ollama 데스크톱 앱을 완전히 종료하고 새 터미널에서 다시 실행합니다.

모델을 다시 다운로드하려면:

```powershell
ollama pull llama3.2:3b
```

이미 모델을 다운로드했다면 기존 `.ollama\models` 안의 `blobs`, `manifests` 폴더를 `C:\OllamaModels`로 복사해도 됩니다.

## 향후 통합 계획

현재 AI Assistant는 독립적으로 동작합니다.

팀원들의 StudentOS 터미널 코드가 올라오면, JSON 명령을 터미널 명령 문자열로 변환한 뒤 터미널 실행 함수에 연결할 수 있습니다.

예시:

```json
{"action": "create_folder", "path": "homework"}
```

터미널 명령:

```text
mkdir homework
```
