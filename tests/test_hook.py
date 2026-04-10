from click.testing import CliRunner
from agentic_pre_commit_hooks.check_agentic_api_spec_documents import main

def test_main_pass():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.py', 'w') as f:
            f.write('def hello(): pass')
        
        result = runner.invoke(main, ['test.py', '--mode', 'check'])
        assert result.exit_code == 0
        assert 'API Spec check passed' in result.output

def test_main_fail():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.py', 'w') as f:
            f.write('# FIXME:api\ndef hello(): pass')
        
        result = runner.invoke(main, ['test.py', '--mode', 'check'])
        assert result.exit_code == 1
        assert 'Error: Undocumented API found' in result.output

def test_main_fix():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('test.py', 'w') as f:
            f.write('# FIXME:api\ndef hello(): pass')
        
        result = runner.invoke(main, ['test.py', '--mode', 'fix'])
        assert result.exit_code == 0
        assert 'Fixing undocumented API' in result.output
        
        with open('test.py', 'r') as f:
            content = f.read()
            assert '# Documented API (Auto-fixed)' in content
