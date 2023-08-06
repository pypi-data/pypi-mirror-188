# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['git_genie']

package_data = \
{'': ['*']}

install_requires = \
['langchain>=0.0.75,<0.0.76',
 'openai>=0.26.4,<0.27.0',
 'tiktoken>=0.1.2,<0.2.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['git-genie = git_genie.main:app']}

setup_kwargs = {
    'name': 'git-genie',
    'version': '0.2.0',
    'description': '',
    'long_description': '# git-genie 🧞\n\nGenerate & explain git commands using plain english.\n\n### Generate commit messages based on staged changes\n\n```shell\n❯ git-genie commit\n\nGenerated command: git commit -m \'Update README with commit message example and instructions\'\n```\n\n### Generate & Explain complex git commands using plain english\n\n![example](example.png)\n\n## Installation\n\n```bash\npip install git-genie\n```\n\n## Usage\n\n`❯ git-genie [OPTIONS] INSTRUCTION`\n\nFor example:\n\n```bash\n❯ git-genie --explain "Who was the last person to modify the README.md file?"\n```\n\nOptions:\n\n- `--explain`, `-e`: Explain the generated git command automatically.\n- `--execute`, `-x`: Execute the generated git command automatically.\n- `--install-completion`: Install completion for the current shell.\n- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n- `--help`, `-h`: Show this message and exit.\n\nIf no options are provided, the program will run in interactive mode.\n\nOptionally, you can add a "gg" alias to your shell\'s rc file (e.g. ~/.bashrc) to make the command shorter:\n\n```bash\nalias gg="git-genie"\n```\n\n### Pre-requisites\n\n#### OpenAI API key\n\n```shell\nexport OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n```\n\n### Generate commit messages\n\nGenerating commit messages is done by using the `commit` command.\nThis method will create a concise message based on the changes staged for a commit.\n\n```bash\n❯ git status\n\nChanges to be committed:\n  (use "git restore --staged <file>..." to unstage)\n        modified:   README.md\n```\n\nLet\'s generate a commit message for the changed README.md file:\n\n```bash\n❯ git-genie commit\nGenerated commit command:git commit -m \'Update README with commit message example and instructions\'\n(E)xplain or e(X)ecute or (N)ew?: X\n```\n\nBy pressing `X`, the generated commit command will be executed automatically:\n\n```bash\nRunning command: git commit -m \'Update README with commit message example and instructions\'\nOutput:\n[commit_gen 75d69ce] Update README with commit message example and instructions\n 1 file changed, 19 insertions(+)\n```\n\n### Interactive mode\n\nBy default, the program will run in interactive mode, where it will ask you if you would like to explain the generated\ngit command, execute it, or generate a new command.\n\n```bash\n~/git-genie ❯ git-genie "count how many times the README.md file was modified in the last week"\n\nGenerated git command: git log --since=1.week -- README.md | grep "^commit" | wc -l\n\n(E)xplain or e(X)ecute or (N)ew?: E\n\nExplanation\n git log -> Show commit logs\n--since=1.week -> Show commits more recent than a specific date\n-- README.md -> Only commits that affect README.md\n| -> Pipe the output of the previous command to the next command\ngrep "^commit" -> Only show lines that start with "commit"\nwc -l -> Count the number of lines\n\ne(X)ecute or (N)ew?: X\n\nRunning command:  git log --since=1.week -- README.md | grep "^commit" | wc -l\nOutput:\n       2\n```\n\n### Non-interactive mode\n\n#### Explain\n\nBy using the `--explain` flag, the program will print the explanation of the generated git command.\n\n```bash\n~/git-genie ❯ git-genie "amend all previous commits with new email address" --explain\n\nGenerated git command:  git rebase -i HEAD~5 --autosquash -m "legacy code"\n\nExplanation\n\n git rebase -> Forward-port local commits to the updated upstream head\n-i, --interactive -> Make a list of the commits which are about to be rebased.Let the user edit that list before rebasing.\n--autosquash -> Automatically move commits that begin with squash!/fixup! to the beginningof the todo list.\n-m, --merge -> Use the given message as the merge commit message.If multiple -m options are given, their values are concatenated as separate paragraphs.\nHEAD~5 -> The last 5 commits\nlegacy code -> The message of the merge commit\n```\n\n#### Execute\n\nBy using the `--execute` flag, the program will execute the generated git command automatically without asking for\nconfirmation.\n\n```bash\n~/git-genie ❯ git-genie "print last 5 commits logs, condensed" --execute\n\nGenerated git command:  git log -5 --oneline\n\nRunning command:  git log -5 --oneline\n\nOutput:\n9a33bc3 update email\nf76f041 CLI interface\nae8abbd Add pycache to gitignore\n67169fd rich print\n3bac238 Refactor\n```\n',
    'author': 'Daniel Palma',
    'author_email': 'danivgy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
