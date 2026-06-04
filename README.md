# software_project

소사 팀플

## StudentOS AI Assistant

The local AI assistant lives in `chatbot/`.

Run the CLI:

```powershell
python -m chatbot.main
```

Run the Tkinter GUI:

```powershell
python -m chatbot.gui
```

The assistant uses Ollama locally, not the OpenAI API. By default it calls:

- model: `llama3.2:3b`
- API URL: `http://localhost:11434/api/generate`

You can override these with environment variables:

```powershell
$env:OLLAMA_MODEL = "llama3.2:3b"
$env:OLLAMA_URL = "http://localhost:11434/api/generate"
```

The AI returns structured JSON such as:

```json
{"action": "create_folder", "path": "homework"}
```

The executor supports only safe filesystem actions:

- `create_file`
- `create_folder`
- `delete_file`
- `delete_folder`
- `list_files`
- `chat`
