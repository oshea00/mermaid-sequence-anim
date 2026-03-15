# Mermaid Sequence Animator

A browser-based tool that turns Mermaid `sequenceDiagram` markup into step-by-step animations rendered on an HTML canvas.

## Overview

Paste or upload a Mermaid sequence diagram and the tool parses it into individual steps — messages, notes, and loop/alt blocks — then animates them one at a time on a canvas with smooth transitions and participant lifelines.

### Features

- **Editor view** — paste Mermaid `sequenceDiagram` text directly or upload a `.md` / `.mmd` / `.txt` file
- **Playback controls** — play, pause, step forward/backward, reset, and adjustable speed (0.5×–3×)
- **Step panel** — sidebar listing every step grouped by phase; click any step to jump to it
- **Progress bar** — scrub to any point in the animation
- **Zoom & pan** — zoom in/out, fit-to-canvas, and click-drag to pan
- **GIF export** — render the full animation to a downloadable GIF

### Running locally

```
python main.py          # serves on http://localhost:8000
python main.py 3000     # or specify a port
```

No dependencies are required beyond Python 3.13+.

## MCP Tool Calls
![sequence Animation](./sequence-animation.gif)

```mermaid
sequenceDiagram
    participant User
    participant Chat as ChatSession
    participant OpenAI as OpenAI API
    participant Executor as MCPToolExecutor<br/>(Translation Layer)
    participant MCP as MCP Server

    User->>Chat: "What's the weather in Paris?"

    Note over Chat,OpenAI: Phase 1: Initial Chat Completion
    Chat->>Chat: Add user message to history
    Chat->>OpenAI: chat.completions.create(<br/>messages=[...],<br/>tools=[...],<br/>tool_choice="auto")
    OpenAI->>Chat: Response with tool_calls array:<br/>[{id: "call_123", function: {<br/>name: "get_weather",<br/>arguments: '{"location": "Paris"}'}}]

    Note over Chat,MCP: Phase 2: Tool Execution via Translation Layer
    Chat->>Chat: Detect tool_calls in response
    Chat->>Chat: Add assistant message with tool_calls to history

    loop For each tool_call
        Chat->>Executor: execute_tool(<br/>"get_weather",<br/>{"location": "Paris"})

        Note over Executor: Translate OpenAI → MCP
        Executor->>Executor: Lookup server for "get_weather"<br/>→ "utilities" server
        Executor->>MCP: stdio_client(command, args)
        Executor->>MCP: session.initialize()
        Executor->>MCP: session.call_tool(<br/>"get_weather",<br/>{"location": "Paris"})
        MCP->>Executor: CallToolResult:<br/>content: [TextContent(<br/>text="Weather in Paris: Sunny, 72°F")]

        Note over Executor: Extract result
        Executor->>Executor: Extract text from content array
        Executor->>Chat: "Weather in Paris: Sunny, 72°F"

        Chat->>Chat: Add tool result to history:<br/>{role: "tool",<br/>tool_call_id: "call_123",<br/>content: "..."}
    end

    Note over Chat,OpenAI: Phase 3: Final Response Synthesis
    Chat->>OpenAI: chat.completions.create(<br/>messages=[..., tool_results])
    OpenAI->>Chat: Final response synthesized<br/>from tool results
    Chat->>User: "The weather in Paris is<br/>sunny with 72°F"
```
