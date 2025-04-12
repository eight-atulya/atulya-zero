

## A ai framework that grows and learns with you

- Atulya Zero is not a predefined ai framework. It is designed to be dynamic, organically growing, and learning as you use it.
- Atulya Zero is fully transparent, readable, comprehensible, customizable, and interactive.
- Atulya Zero uses the computer as a tool to accomplish its (your) tasks.

# 💡 Key Features

1. **General-purpose Assistant**

- Atulya Zero is not pre-programmed for specific tasks (but can be). It is meant to be a general-purpose personal assistant. Give it a task, and it will gather information, execute commands and code, cooperate with other atulya instances, and do its best to accomplish it.
- It has a persistent memory, allowing it to memorize previous solutions, code, facts, instructions, etc., to solve tasks faster and more reliably in the future.


2. **Computer as a Tool**

- Atulya Zero uses the operating system as a tool to accomplish its tasks. It has no single-purpose tools pre-programmed. Instead, it can write its own code and use the terminal to create and use its own tools as needed.
- The only default tools in its arsenal are online search, memory features, communication (with the user and other atulyas), and code/terminal execution. Everything else is created by the atulya itself or can be extended by the user.
- Tool usage functionality has been developed from scratch to be the most compatible and reliable, even with very small models.
- **Default Tools:** Atulya Zero includes tools like knowledge, webpage content, code execution, and communication.
- **Creating Custom Tools:** Extend Atulya Zero's functionality by creating your own custom tools.
- **Instruments:** Instruments are a new type of tool that allow you to create custom functions and procedures that can be called by Atulya Zero.

3. **Multi-atulya Cooperation**

- Every atulya has a superior atulya giving it tasks and instructions. Every atulya then reports back to its superior.
- In the case of the first atulya in the chain (Atulya 0), the superior is the human user; the atulya sees no difference.
- Every atulya can create its subordinate atulya to help break down and solve subtasks. This helps all atulyas keep their context clean and focused.


4. **Completely Customizable and Extensible**

- Almost nothing in this framework is hard-coded. Nothing is hidden. Everything can be extended or changed by the user.
- The whole behavior is defined by a system prompt in the **prompts/default/atulya.system.md** file. Change this prompt and change the framework dramatically.
- The framework does not guide or limit the atulya in any way. There are no hard-coded rails that atulyas have to follow.
- Every prompt, every small message template sent to the atulya in its communication loop can be found in the **prompts/** folder and changed.
- Every default tool can be found in the **python/tools/** folder and changed or copied to create new predefined tools.


5. **Communication is Key**

- Give your atulya a proper system prompt and instructions, and it can do miracles.
- Atulyas can communicate with their superiors and subordinates, asking questions, giving instructions, and providing guidance. Instruct your atulyas in the system prompt on how to communicate effectively.
- The terminal interface is real-time streamed and interactive. You can stop and intervene at any point. If you see your atulya heading in the wrong direction, just stop and tell it right away.
- There is a lot of freedom in this framework. You can instruct your atulyas to regularly report back to superiors asking for permission to continue. You can instruct them to use point-scoring systems when deciding when to delegate subtasks. Superiors can double-check subordinates' results and dispute. The possibilities are endless.

## 🚀 Things you can build with Atulya Zero

- **Development Projects** - `"Create a React dashboard with real-time data visualization"`

- **Data Analysis** - `"Analyze last quarter's NVIDIA sales data and create trend reports"`

- **Content Creation** - `"Write a technical blog post about microservices"`

- **System Admin** - `"Set up a monitoring system for our web servers"`

- **Research** - `"Gather and summarize five recent AI papers about CoT prompting"`

# ⚙️ Installation



A detailed setup guide for Windows, macOS, and Linux with a video can be found in the Atulya Zero Documentation at [this page](./docs/installation.md).

### ⚡ Quick Start

```bash
# Pull and run with Docker

docker pull eight-atulya/atulya-zero-run
docker run -p 50001:80 eight-atulya/atulya-zero-run

# Visit http://localhost:50001 to start
```

- Developers and contributors: download the full binaries for your system from the [releases page](https://github.com/eight-atulya/atulya-zero/releases) and then follow the instructions [provided here](./docs/installation.md#in-depth-guide-for-full-binaries-installation).

## 🐳 Fully Dockerized, with Speech-to-Text and TTS


- Customizable settings allow users to tailor the atulya's behavior and responses to their needs.
- The Web UI output is very clean, fluid, colorful, readable, and interactive; nothing is hidden.
- You can load or save chats directly within the Web UI.
- The same output you see in the terminal is automatically saved to an HTML file in **logs/** folder for every session.


- Atulya output is streamed in real-time, allowing users to read along and intervene at any time.
- No coding is required; only prompting and communication skills are necessary.
- With a solid system prompt, the framework is reliable even with small models, including precise tool usage.

## 👀 Keep in Mind

1. **Atulya Zero Can Be Dangerous!**

- With proper instruction, Atulya Zero is capable of many things, even potentially dangerous actions concerning your computer, data, or accounts. Always run Atulya Zero in an isolated environment (like Docker) and be careful what you wish for.

2. **Atulya Zero Is Not Pre-programmed; It Is Prompt-based.**

- The whole framework contains only a minimal amount of code and does not guide the atulya in any way. Everything lies in the system prompt located in the **prompts/** folder.

3. **If You Cannot Provide the Ideal Environment, Let Your Atulya Know.**

- Atulya Zero is made to be used in an isolated virtual environment (for safety) with some tools preinstalled and configured.

### 📌 Known Problems

1. The system prompt may need improvements; contributions are welcome!
2. The atulya may inadvertently alter its operating environment; cleaning up the `work_dir` often fixes this.
3. Atulyas might loop in multi-ai interactions, leading to unexpected behaviors.

## 📚 Read the Documentation

| Page | Description |
|-------|-------------|
| [Installation](./docs/installation.md) | Installation, setup and configuration |
| [Usage](./docs/usage.md) | Basic and advanced usage |
| [Architecture](./docs/architecture.md) | System design and components |
| [Contributing](./docs/contributing.md) | How to contribute |
| [Troubleshooting](./docs/troubleshooting.md) | Common issues and their solutions |

