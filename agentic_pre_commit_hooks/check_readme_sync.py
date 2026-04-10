import subprocess
import sys
import json
import click

def get_git_diff() -> str:
    """Captures the git diff of staged changes."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error capturing diff: {e}"

@click.command()
@click.argument('filenames', nargs=-1)
def main(filenames: tuple[str, ...]) -> None:
    """
    Uses the Copilot CLI to check if the README matches the implementation.
    Includes the git diff in the analysis for better accuracy.
    """
    click.echo("🚀 Running Smarter Agentic README Sync Check...")

    diff = get_git_diff()
    if not diff.strip():
        click.echo("No staged changes to check.")
        sys.exit(0)

    # Constructing a more sophisticated prompt
    prompt = f"""Analyze the following Git diff against the README.md.
Does the README still accurately reflect the code changes? 
Focus on usage examples, technical details, and architectural changes. 
Reply only with 'MATCHED' or 'MISMATCHED' followed by a short reason.

--- GIT DIFF ---
{diff[:4000]}"""
    
    def extract_agent_text(data):
        """Recursively extracts text content from nested JSON objects."""
        if isinstance(data, str):
            return data
        if not isinstance(data, dict):
            return ""
        
        # Check known text fields
        for field in ["content", "text", "message", "value"]:
            if field in data and isinstance(data[field], str):
                return data[field]
        
        # Recurse into 'data' or 'payload' if they exist
        for field in ["data", "payload"]:
            if field in data and isinstance(data[field], dict):
                return extract_agent_text(data[field])
        
        return ""

    try:
        # Run copilot with JSON output format
        result = subprocess.run(
            ["copilot", "-p", prompt, "--output-format", "json"],
            capture_output=True,
            text=True,
            check=False
        )

        full_output = result.stdout
        error_output = result.stderr
        
        # Parse JSONL output
        agent_response = ""
        try:
            for line in full_output.strip().split('\n'):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    # Only parse types that represent the assistant's response to avoid echoing the prompt
                    if data.get("type") in ["assistant.message", "text", "chunk", "message"]:
                        agent_response += extract_agent_text(data)
                except json.JSONDecodeError:
                    continue 
        except Exception:
            pass

        # If agent_response is still empty, fallback to full_output (but try to avoid repeating the prompt)
        if not agent_response.strip():
            agent_response = full_output.strip()

        # Final decision logic
        clean_response = agent_response.upper()
        if "MATCHED" in clean_response and "MISMATCHED" not in clean_response:
            if agent_response.strip():
                click.echo(f"🤖 Copilot Reasoning:\n{agent_response.strip()}")
            click.secho("\n✅ README is in sync with the implementation.", fg='green', bold=True)
            sys.exit(0)
        else:
            click.secho("\n❌ README mismatch detected!", fg='red', bold=True)
            if agent_response.strip():
                # If the reasoning repeating the prompt, try a simple heuristic to show only the end
                display_response = agent_response.strip()
                if "--- GIT DIFF ---" in display_response:
                    display_response = display_response.split("--- GIT DIFF ---")[-1].split("\n", 1)[-1]
                click.echo(f"🤖 Copilot Analysis:\n{display_response.strip()}")
            elif error_output.strip():
                click.secho(f"⚠️  CLI Error Output:\n{error_output.strip()}", fg='yellow')
            else:
                click.echo("🤖 No detailed analysis received from Copilot.")
            sys.exit(1)

    except FileNotFoundError:
        click.secho("❌ Error: 'copilot' CLI not found in PATH.", fg='red')
        sys.exit(1)
    except Exception as e:
        click.secho(f"❌ Error during execution: {e}", fg='red')
        sys.exit(1)

if __name__ == '__main__':
    main()
