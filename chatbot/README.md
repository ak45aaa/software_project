# StudentOS AI Assistant

This package converts natural language into structured StudentOS commands.

Flow:

```text
user text -> local Ollama model -> JSON command -> safe executor
```

Example:

```json
{"action": "create_folder", "path": "homework"}
```

## Files

- `chatbot.py`: Ollama API client and `parse_command()`
- `command_parser.py`: JSON extraction, normalization, and simple rule-based parsing
- `command_executor.py`: safe filesystem executor with no arbitrary shell execution
- `main.py`: CLI entrypoint
- `gui.py`: Tkinter GUI entrypoint

## Run

Start Ollama first, then run one of:

```powershell
python -m chatbot.main
python -m chatbot.gui
```

## Ollama Notes For Korean Windows Usernames

If Ollama fails with a path like `C:\Users\����\.ollama\...`, move model storage to an ASCII path:

```powershell
mkdir C:\OllamaModels
setx OLLAMA_MODELS C:\OllamaModels
```

Then close the Ollama desktop app completely and restart Ollama from a new terminal. If the model was already downloaded, copy the old `blobs` and `manifests` folders into `C:\OllamaModels`; otherwise run:

```powershell
ollama pull llama3.2:3b
```
