### Standard Message Flow (No Tools)

```mermaid
sequenceDiagram
    participant User
    participant Chat as ChatSession
    participant LLM as OpenAI LLM
    
    User->>Chat: Enter message
    Chat->>LLM: Send message + available tools
    LLM->>Chat: Response (no tool calls)
    Chat->>User: Display response
```

