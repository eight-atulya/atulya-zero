<div align="center">

![Atulya Zero](/docs/res/header.png)

[Installation](./docs/installation.md) • [How to Update](./docs/installation.md#how-to-update-atulya-zero) • [Documentation](./docs/README.md) • [Usage](./docs/usage.md)

</div>

> [!NOTE]
> **🎉 v0.0.0.1 Release**: Now featuring Atulya capable of using Chromium for web interactions! This enables Atulya to browse the web, gather information, and interact with web content autonomously.

---

# 🌱 A Personal, Organic AI Framework That Grows and Learns With You

- Atulya is not a predefined AI framework. It is designed to be dynamic, organically growing, and learning as you use it.
- Fully transparent, readable, comprehensible, customizable, and interactive.
- Uses the computer as a tool to accomplish its (your) tasks.

---

# 💡 Key Features

## 1. General-purpose Assistant

- Atulya is not pre-programmed for specific tasks (but can be). It is meant to be a general-purpose personal assistant. Give it a task, and it will gather information, execute commands and code, cooperate with other Atulya instances, and do its best to accomplish it.
- Persistent memory allows it to memorize previous solutions, code, facts, instructions, etc., to solve tasks faster and more reliably in the future.

## 2. Computer as a Tool

- Atulya uses the operating system as a tool to accomplish its tasks. It has no single-purpose tools pre-programmed. Instead, it can write its own code and use the terminal to create and use its own tools as needed.
- **Default Tools:** Includes knowledge, webpage content, code execution, and communication.
- **Creating Custom Tools:** Extend functionality by creating your own custom tools.
- **Instruments:** A new type of tool that allows you to create custom functions and procedures that can be called by Atulya Zero.

## 3. Multi-Atulya Cooperation

- Every Atulya has a superior Atulya giving it tasks and instructions. Every Atulya then reports back to its superior.
- The first Atulya in the chain (Atulya 0) interacts directly with the human user.
- Subordinate Atulyas help break down and solve subtasks, keeping context clean and focused.

## 4. Completely Customizable and Extensible

- Almost nothing in this framework is hard-coded. Everything can be extended or changed by the user.
- The whole behavior is defined by a system prompt in the **prompts/default/atulya.system.md** file. Change this prompt to dramatically alter the framework.
- Every prompt, message template, and default tool can be found in the **prompts/** and **python/tools/** folders for customization.

## 5. Communication is Key

- Proper system prompts and instructions enable Atulya to perform complex tasks.
- Atulyas communicate with their superiors and subordinates, asking questions, giving instructions, and providing guidance.
- The terminal interface is real-time streamed and interactive, allowing users to intervene at any point.

---

# 🚀 Things You Can Build With Atulya Zero

- **Development Projects** - "Create a React dashboard with real-time data visualization."
- **Data Analysis** - "Analyze last quarter's NVIDIA sales data and create trend reports."
- **Content Creation** - "Write a technical blog post about microservices."
- **System Admin** - "Set up a monitoring system for our web servers."
- **Research** - "Gather and summarize five recent AI papers about CoT prompting."

---

# ⚙️ Installation

Click to open a video to learn how to install Atulya Zero:

A detailed setup guide for Windows, macOS, and Linux with a video can be found in the Atulya Zero Documentation at [this page](./docs/installation.md).

### ⚡ Quick Start

```bash
# Pull and run with Docker
docker pull eight-atulya/atulya-zero-run
docker run -p 50001:80 eight-atulya/atulya-zero-run

# Visit http://localhost:50001 to start
```

- Developers and contributors: download the full binaries for your system from the [releases page](https://github.com/eight-atulya/atulya-zero/releases) and then follow the instructions [provided here](./docs/installation.md#in-depth-guide-for-full-binaries-installation).

---

# 🐳 Fully Dockerized, With Speech-to-Text and TTS

- Customizable settings allow users to tailor Atulya's behavior and responses to their needs.
- The Web UI output is clean, fluid, colorful, readable, and interactive.
- Load or save chats directly within the Web UI.
- Session outputs are automatically saved to an HTML file in the **logs/** folder.
- No coding is required; only prompting and communication skills are necessary.

---

# 👀 Keep in Mind

## 1. Atulya Zero Can Be Dangerous!

- With proper instruction, Atulya Zero is capable of many things, even potentially dangerous actions concerning your computer, data, or accounts. Always run Atulya Zero in an isolated environment (like Docker) and be careful what you wish for.

## 2. Atulya Zero Is Prompt-based.

- The whole framework is guided by the **prompts/** folder. Atulya guidelines, tool instructions, messages, utility AI functions, it's all there.

---

# 📚 Read the Documentation

| Page | Description |
|-------|-------------|
| [Installation](./docs/installation.md) | Installation, setup, and configuration |
| [Usage](./docs/usage.md) | Basic and advanced usage |
| [Architecture](./docs/architecture.md) | System design and components |
| [Contributing](./docs/contributing.md) | How to contribute |
| [Troubleshooting](./docs/troubleshooting.md) | Common issues and their solutions |

