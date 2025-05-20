# agent-native/IDE Specification

## Project Title
**agent-native/IDE**

## Author
TBD

## Last Updated
TBD

---

## 1. Objective

Build a lightweight, terminal-based code editor designed for **AI agents** to read, edit, and run code in a controlled and observable environment.

This tool will offer simple, well-defined editing primitives and a traceable, reproducible state model. The IDE should allow humans to observe agent actions but will prioritize agent use, not human interaction.

---

## 2. Scope

### In Scope
- Text buffer management (load, edit, insert, delete)
- File tree scanning and folder expansion/collapse
- Terminal command execution and output capture
- Undo/redo functionality
- TUI frontend using Textual (minimal, for debugging by humans)
- Exposing simple agent tools (e.g., `replace_line`, `run_command`)
- State export for inspection/debugging

### Out of Scope
- Language Server Protocol (LSP) integration
- Syntax highlighting beyond plain text
- Human-oriented IDE features (minimap, folding, themes)
- End-to-end agent orchestration

---

## 3. Requirements

### 3.1 Functional Requirements
- Load a file into an editor buffer.
- Replace, insert, and delete lines in the buffer.
- Scroll through the buffer.
- Display a navigable file tree of the workspace.
- Expand/collapse directories in the file tree.
- Select a file from the tree and load it into the editor.
- Run shell commands in an isolated environment and capture output.
- Provide undo and redo functionality using full-state snapshots.
- Expose all editing and navigation functions as simple Python functions.

### 3.2 Non-Functional Requirements
- Minimal runtime memory and CPU usage.
- Fast startup (<1 second).
- Robust against invalid operations (e.g., out-of-bounds edits).
- Logs of all state changes for debugging and replay.
- Logs of all traces from LLMs

---

## 4. Interfaces

All core components must implement abstract base classes (interfaces) under `/interfaces` to allow testing, mocking, and future extensibility.

| Interface | Responsibilities |
|:----------|:-----------------|
| `IEditorBuffer` | Manage lines of text loaded from a file. |
| `IFileTree` | Represent and navigate file system structure. |
| `ITerminalRunner` | Execute shell commands and return outputs. |
| `IUndoManager` | Manage undo/redo functionality. |

Each interface must be pure (only define behavior, no state).

---

## 5. Components

| Component | Responsibilities |
|:----------|:-----------------|
| `EditorBuffer` | Concrete implementation of `IEditorBuffer`. |
| `FileTreeModel` | Concrete implementation of `IFileTree`. |
| `TerminalRunner` | Concrete implementation of `ITerminalRunner`. |
| `ActionUndoManager` | Concrete implementation of `IUndoManager`. |
| `IDEState` | Aggregate object that holds the current editor, file tree, terminal, and undo manager. |

---

## 6. APIs (Agent Tools)

The following functions must be exposed in `/tools`:

| Tool Function | Description |
|:--------------|:------------|
| `replace_line(line_num: int, new_text: str)` | Replace a specific line in the editor. |
| `append_after(line_num: int, new_text: str)` | Insert a line after a given line. |
| `scroll(lines: int)` | Scroll the editor view by a number of lines. |
| `expand_folder(path: str)` | Expand a folder in the file tree. |
| `collapse_folder(path: str)` | Collapse a folder in the file tree. |
| `select_file(path: str)` | Load a new file into the editor buffer. |
| `run_command(command: str)` | Execute a terminal command. |
| `undo()` | Undo last change. |
| `redo()` | Redo last undone change. |
| `get_context()` | Return serialized state of IDE. |

Each function must accept an `IDEState` object explicitly or through a context manager.

---

## 7. Data Models

### 7.1 Snapshot Model
Each snapshot must contain:
- Editor buffer (list of strings)
- File tree structure (simple dict or nested list)
- Terminal last command and output
- Active file path

### 7.2 Trace Model
Each trace must contain:
- Tool use (arguments + tool) OR
- Text content (if it's a conversation -> thinking)
- A list of traces will be the "save"
---

## 8. Dependencies

| Dependency | Purpose |
|:-----------|:--------|
| `textual` | Terminal-based UI rendering (optional, not mandatory) |
| `python 3.10+` | Typing improvements, standard library usage |
| `pytest` | Testing |
| `black`, `isort` | Code formatting |

Optional (future):
- `pygments` for syntax highlighting
- `FastAPI` for exposing HTTP APIs

---

## 9. Testing Plan

- Unit tests for each tool and core component.
- Mock terminal outputs and filesystem for testing.
- Test undo/redo with random edit sequences.
- Docker integration test (start IDE inside a container and execute dummy edits).

Minimum target: 90% unit test coverage.

---

## 10. Deliverables

- `/core` — Core logic classes
- `/interfaces` — ABCs for all components
- `/tools` — Agent-friendly function API
- `/textual_ui` — Optional TUI frontend
- `/tests` — Full test suite
- `/examples` — Sample agent scripts
- `README.md` — Full project description

---

## 11. Milestones

| Milestone | Target Date |
|:----------|:------------|
| IDE Core classes complete | TBD |
| Agent Tool layer complete | TBD |
| Unit tests complete | TBD |
| Textual TUI MVP | TBD |
| Docker image ready | TBD |
| First public release (v0.1) | TBD |

---

## 12. Risks and Mitigations

| Risk | Mitigation |
|:-----|:-----------|
| Agents need more complex features later (e.g., syntax) | Design extensible interfaces |
| Security vulnerabilities in terminal execution | Sandbox commands inside container |
| Slow agent adoption | Focus on clean docs, good examples, simple demos |
