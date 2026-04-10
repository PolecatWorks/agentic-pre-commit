import subprocess
import sys
import click

@click.command()
@click.argument('filenames', nargs=-1)
def main(filenames: tuple[str, ...]) -> None:
    """
    Uses the Copilot CLI to check if the README matches the implementation.
    """
    click.echo("🚀 Running Agentic README Sync Check via Copilot...")

    prompt = "Does the README match the code? Reply only with 'MATCHED' or 'MISMATCHED'"
    
    try:
        # Execute the copilot prompt in non-interactive mode
        # We capture stdout and stderr to process the response
        result = subprocess.run(
            ["copilot", "-p", prompt],
            capture_output=True,
            text=True,
            check=False
        )

        output = result.stdout
        error_output = result.stderr

        # Check for 'MATCHED' in the output (equivalent to grep -qw "MATCHED")
        if "MATCHED" in output and "MISMATCHED" not in output:
            click.secho("\n✅ README appears to be in sync with the implementation.", fg='green', bold=True)
            sys.exit(0)
        else:
            if output:
                click.echo(f"🤖 Copilot Response:\n{output.strip()}")
            if error_output:
                click.echo(f"⚠️  Stderr:\n{error_output.strip()}")
                
            click.secho("\n❌ README mismatch detected or Copilot could not confirm sync!", fg='red', bold=True)
            sys.exit(1)

    except FileNotFoundError:
        click.secho("❌ Error: 'copilot' CLI not found in PATH.", fg='red')
        sys.exit(1)
    except Exception as e:
        click.secho(f"❌ Error executing Copilot: {e}", fg='red')
        sys.exit(1)

if __name__ == '__main__':
    main()
