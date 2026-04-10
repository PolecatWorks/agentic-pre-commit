import pytest
from click.testing import CliRunner
from pre_commit_hooks.check_agentic_api_spec_documents import main

def test_main_pass():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.py', 'w') as f:
            f.write('def hello(): pass')
        
        result = runner.invoke(main, ['test.py'])
        assert result.exit_code == 0
        assert 'API Spec validation passed' in result.output

def test_main_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.py', 'w') as f:
            f.write('# FIXME:api\ndef hello(): pass')
        
        result = runner.invoke(main, ['test.py'])
        assert result.exit_code == 1
        assert 'Error: Undocumented API found' in result.output
