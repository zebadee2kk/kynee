# Handover: VSCode (with Copilot)

## Profile
- **Strengths**: Integrated IDE, extensions, debugging, Git integration
- **Token Limit**: N/A (IDE, not AI)
- **Session Cost**: Free (open-source)
- **Best For**: Day-to-day development, debugging, testing
- **AI Features**: GitHub Copilot, Copilot Chat, IntelliSense

---

## Setup Instructions

### 1. Install VSCode
```bash
# macOS
brew install --cask visual-studio-code

# Linux (Debian/Ubuntu)
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code

# Windows
winget install Microsoft.VisualStudioCode
```

### 2. Install Extensions

**Essential**:
- **Python** (ms-python.python): Linting, debugging, testing
- **Pylance** (ms-python.vscode-pylance): Fast IntelliSense
- **GitHub Copilot** (github.copilot): AI autocomplete
- **ESLint** (dbaeumer.vscode-eslint): JavaScript linting
- **Prettier** (esbenp.prettier-vscode): Code formatting
- **YAML** (redhat.vscode-yaml): YAML schema validation
- **Docker** (ms-azuretools.vscode-docker): Dockerfile support

**Recommended**:
- **GitLens** (eamodio.gitlens): Advanced Git features
- **Better Comments** (aaron-bond.better-comments): Highlight TODOs
- **Error Lens** (usernamehw.errorlens): Inline error messages
- **Markdown All in One** (yzhang.markdown-all-in-one): Markdown editing

**Install via CLI**:
```bash
code --install-extension ms-python.python
code --install-extension github.copilot
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode
code --install-extension redhat.vscode-yaml
code --install-extension ms-azuretools.vscode-docker
```

### 3. Workspace Configuration

Create `.vscode/settings.json` in repo root:

```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/agent/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["agent/tests"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true,
    "**/node_modules": true
  },
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "markdown": true
  }
}
```

---

## Development Workflow

### Daily Tasks

#### 1. Open Workspace
```bash
cd ~/projects/kynee
code .
```

#### 2. Activate Virtual Environment
- Terminal in VSCode: Ctrl+` (backtick)
- Python interpreter: Ctrl+Shift+P → "Python: Select Interpreter" → Choose `agent/venv`

#### 3. Run Tests
- Test Explorer: Click beaker icon in sidebar
- Run all: Click play button
- Debug test: Right-click test → "Debug Test"

#### 4. Debugging
- Set breakpoint: Click left of line number
- Start debugging: F5
- Step over: F10, Step into: F11, Continue: F5

#### 5. Git Operations
- Source Control: Ctrl+Shift+G
- Stage changes: Click `+` next to file
- Commit: Ctrl+Enter
- Push: Click `...` → "Push"

---

## Keyboard Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| Command Palette | Cmd+Shift+P | Ctrl+Shift+P |
| Quick Open File | Cmd+P | Ctrl+P |
| Toggle Terminal | Ctrl+` | Ctrl+` |
| Find in Files | Cmd+Shift+F | Ctrl+Shift+F |
| Go to Definition | F12 | F12 |
| Rename Symbol | F2 | F2 |
| Format Document | Shift+Alt+F | Shift+Alt+F |
| Toggle Comment | Cmd+/ | Ctrl+/ |
| Multi-Cursor | Cmd+D | Ctrl+D |
| Copilot Suggest | Tab | Tab |
| Copilot Next | Alt+] | Alt+] |

---

## Recommended Tasks

### Weekly
- [ ] Update extensions: Ctrl+Shift+X → Check for updates
- [ ] Review linting errors: Problems panel (Ctrl+Shift+M)
- [ ] Run full test suite: Test Explorer → Run All
- [ ] Check test coverage: Terminal → `pytest --cov-report=html`

### Monthly
- [ ] Clean up workspace: Delete `__pycache__`, `node_modules/.cache`
- [ ] Review Copilot stats: GitHub settings → Copilot usage
- [ ] Update VSCode: Help → Check for Updates

---

## Integration with AI Coders

### With GitHub Copilot
- **Inline suggestions**: Accept with Tab, reject with Esc
- **Copilot Chat**: Ctrl+Shift+I → Ask questions about code
- **Generate tests**: Highlight function → Chat: "Write pytest for this"

### With Claude (via Cline extension)
- Install: `saoudrizwan.claude-dev`
- Use: Ctrl+Shift+P → "Cline: Open Chat"
- Features: Multi-file edits, terminal commands, autonomous tasks

### With ChatGPT (via web)
- Copy code from VSCode
- Paste in ChatGPT: "Explain this function"
- Copy response back to comments

---

## Debugging Common Issues

### Python Import Errors
- Fix: Ensure virtual environment activated
- Check: `which python` points to `agent/venv/bin/python`

### Linting Not Working
- Fix: Install ruff: `pip install ruff`
- Check: `.vscode/settings.json` has `python.linting.ruffEnabled: true`

### Tests Not Discovered
- Fix: Set pytest path: `"python.testing.pytestArgs": ["agent/tests"]`
- Refresh: Test Explorer → Reload icon

### Copilot Not Suggesting
- Fix: Check Copilot status: Bottom right corner (should say "Copilot: Ready")
- Re-auth: Ctrl+Shift+P → "GitHub Copilot: Sign In"

---

## Success Criteria

- [ ] VSCode opens workspace with correct interpreter
- [ ] Tests run in Test Explorer
- [ ] Copilot provides suggestions
- [ ] Linting shows errors inline
- [ ] Debugging works with breakpoints

---

**Status**: 🟢 ACTIVE (primary IDE)  
**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk
