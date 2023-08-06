# 🧞‍♂️ Shell Genie

_Your wishes are my commands._

Shell Genie is a command-line tool that lets you interact with the terminal in plain English. You ask the genie what you want to do and it will generate the command for you.

## Installation

The recommended way to install is using [pipx](https://pypa.github.io/pipx/):

1. Install Python 3.10 or higher.
2. Install [pipx](https://github.com/pypa/pipx#install-pipx).
3. Install Shell Genie: `pipx install shell-genie`

Alternatively, you can install it using pip:

1. Install Python 3.10 or higher.
2. Install Shell Genie: `pip install shell-genie`

## How to use

1. First, you need to initialize the tool by running the following command:

   ```shell
   shell-genie init
   ```

   This will prompt you to select a backend (either `openai-gpt3` or `free-genie`) and provide any additional information that is required (e.g. your own [OpenAI API](https://openai.com/api/) key for `openai-gpt3`).

   The `free-genie` backend is free to use. I'm hosting, but as you can imagine I'm not a big corporation with unlimited money, so there's no guarantee that it will be available at all times. My goal is to generate a dataset of commands to fine-tune a model later on (this is mentioned during the initialization process).

2. Once you have initialized the tool, you can start asking the genie what you want to do. For example, you may ask it to find all the `json` files in the current directory that are larger than 1MB:

   ```shell
   shell-genie ask "find all json files in the current directory that are larger than 1MB"
   ```

   You'll see an output similar to this:

   ```shell
   Command: find . -name "*.json" -size +1M
   Do you want to run this command? [y/n]:
   ```

   If you have questions about how the command works, you can ask the genie to explain it:

   ```shell
   shell-genie ask "find all json files in the current directory that are larger than 1MB" --explain
   ```

   And you'll see an output similar to this:

   ```shell
   Command: find . -name "*.json" -size +1M
   Description: This command will search the current directory for all... (shortened for brevity)
   Do you want to run the command? [y/n]:
   ```

3. Run the command if you want to. If you're using `free-genie`, and you want to help improve the tool, you can provide feedback after you've run the command.

## Examples

Here's a short video showing how to use the tool:

[![asciicast](https://asciinema.org/a/438574.svg)](https://asciinema.org/a/438574)
