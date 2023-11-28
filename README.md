# Translator

## Overview
This project is an exploration of the OpenAI API, centered around building a simple, multilingual translation program. The primary goal is to gain hands-on experience with OpenAI's capabilities while developing a practical application.

This README serves as a comprehensive guide and a repository for personal notes regarding the development process.

## Learning Objectives
- Understanding and utilizing the OpenAI API.
- Developing a multilingual translation tool.
- Implementing best practices in API usage and key management.

## Steps for Setup

### 1. Install OpenAI Library and Configure API Key
- **Installation**: Use `pip` to install the OpenAI Python library.
  ```bash
  pip install openai
# Translator

## Overview
This project is an exploration of the OpenAI API, centered around building a simple, multilingual translation program. The primary goal is to gain hands-on experience with OpenAI's capabilities while developing a practical application.

This README serves as a comprehensive guide and a repository for personal notes regarding the development process.

## Learning Objectives
- Understanding and utilizing the OpenAI API.
- Developing a multilingual translation tool.
- Implementing best practices in API usage and key management.

## Steps for Setup

### 1. Install OpenAI Library and Configure API Key
- **Installation**: Use `pip` to install the OpenAI Python library.
  ```bash
  pip install openai

### NOTE: To ensure that VSCode inherits the environment variables set in your .zshrc file, first navigate to your project directory using the terminal. Then launch VSCode with the code . command. This is important because environment variables defined in .zshrc are loaded into the terminal's environment, and starting VSCode directly from the terminal ensures it inherits these variables. If you start VSCode from a desktop icon or other GUI method, it may not have access to the same set of environment variables.

<!-- Main idea is now to build a live translator to other languages,, speed is initial concern
OpenAI API whisper-1 only translates to english but -->

### Be sure to specify --language, if not whisper will take first 30 seconds of audio and try to detect itself but not always accurate + slower solution. User should specify input and output language then
**whisper SpanishAudio.mp3 --model large --language Spanish**
