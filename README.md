# Agentic Pre-commit 🤖🛡️

> **Harness the power of AI agents directly in your Git workflow.**

`Agentic Pre-commit` is a specialized [pre-commit](https://pre-commit.com) hook designed to run sophisticated AI agent actions on your staged changes. By leveraging Python and Copilot-driven intelligence, it moves beyond simple static analysis to provide context-aware feedback, automated refactoring, and intelligent code validation.

---

## 🌟 Features

- **AI-Driven Analysis**: Uses LLM-powered agents to understand the *intent* of your code, not just the syntax.
- **Copilot Integration**: Leverages Copilot's advanced reasoning to perform complex tasks like security audits, performance profiling, and logic verification.
- **Automated Refactoring**: Option to allow agents to automatically suggest or apply non-trivial improvements.
- **Contextual Documentation**: Automatically detects when documentation is out of sync with code changes.
- **Customizable Agent Actions**: Define specific "missions" for the AI to execute during the pre-commit phase.

## 🚀 Getting Started

### Prerequisites

- [Python 3.9+](https://www.python.org/)
- [pre-commit](https://pre-commit.com/#install)
- An active GitHub Copilot subscription (or compatible AI backend)

### Installation

1.  **Add to your `.pre-commit-config.yaml`**:

    ```yaml
    repos:
      - repo: https://github.com/polecatworks/Agentic-pre-commit
        rev: v0.1.0  # Use the latest version
        hooks:
          - id: agentic-api-spec-check
    ```

2.  **Install the hooks**:

    ```bash
    # Install the pre-commit hook
    pre-commit install

    # Install the pre-push hook
    pre-commit install --hook-type pre-push
    ```

## 🛠️ Configuration

You can customize the behavior of the agent by adding a configuration file or passing arguments in your hook definition.

### Available Modes

| Mode | Description |
| :--- | :--- |
| `check` | (Default) Performs a scan and fails the commit if issues are found. |
| `fix` | Automatically attempts to fix common issues (e.g. placeholder tags). |

## 🧩 How It Works

1.  **Stage Changes**: You run `git add .`
2.  **Trigger Hook**: You run `git commit`.
3.  **Agent Initialization**: The script initializes a Python-based LangGraph/LangChain agent.
4.  **AI Execution**: The agent receives the diff of the staged files and executes the requested actions using Copilot.
5.  **Validation**: If the agent finds issues (and `fix` mode is off), the commit is blocked with a detailed report.

## 💻 Development

### Local Testing
When developing hooks in this repository, use the `local` repo type in your `.pre-commit-config.yaml` to test changes without pushing:

```yaml
repos:
  - repo: local
    hooks:
      - id: agentic-api-spec-documents
        name: Check API specs are documented
        entry: ./venv/bin/check-agentic-api-spec
        language: script
        types: [python]
```

### Running Tests
This project uses `pytest` for testing. Run the test suite with:

```bash
poetry run pytest
```

## 🤝 Contributing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by <a href="https://github.com/polecatworks">PolecatWorks</a>
</p>
