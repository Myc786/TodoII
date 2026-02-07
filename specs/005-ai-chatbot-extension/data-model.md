# Data Model: AI-Powered Todo Chatbot Extension

**Feature**: AI-Powered Todo Chatbot Extension
**Date**: 2026-01-17

## Entity: ChatMessage
Represents a single message in the chatbot conversation

### Fields:
- `id` (string): Unique identifier for the message
- `sender` (enum: "user" | "ai"): Identifies the message sender
- `content` (string): The text content of the message
- `timestamp` (datetime): When the message was created
- `userId` (string): ID of the authenticated user
- `sessionId` (string): ID of the chat session
- `intent` (string, optional): The recognized intent of the message
- `toolCall` (object, optional): Details of any MCP tool call made

### Relationships:
- Belongs to a `ChatSession`
- Associated with a `User`

### Validation Rules:
- `content` must be non-empty
- `sender` must be either "user" or "ai"
- `timestamp` must be in ISO format
- `userId` must match authenticated user

## Entity: ChatSession
Represents a single chat session with a user

### Fields:
- `id` (string): Unique identifier for the session
- `userId` (string): ID of the user for this session
- `createdAt` (datetime): When the session was created
- `lastActivityAt` (datetime): Last activity in the session
- `isActive` (boolean): Whether the session is currently active

### Relationships:
- Contains many `ChatMessage`s
- Associated with a `User`

### Validation Rules:
- `userId` must match authenticated user
- `isActive` defaults to true

## Entity: UserIntent
Represents the interpreted purpose of a user message

### Fields:
- `id` (string): Unique identifier for the intent
- `type` (enum: "create_task" | "list_tasks" | "complete_task" | "delete_task" | "query_status"): Type of intent
- `confidence` (number): Confidence level of intent recognition (0-1)
- `parameters` (object): Extracted parameters from the user input
- `originalMessage` (string): Original user input
- `processedAt` (datetime): When the intent was processed

### Relationships:
- Associated with a `ChatMessage`

### Validation Rules:
- `type` must be one of the allowed enum values
- `confidence` must be between 0 and 1
- `parameters` must match expected structure for intent type

## Entity: MCPToolCall
Represents a call to an MCP tool

### Fields:
- `id` (string): Unique identifier for the tool call
- `toolName` (string): Name of the MCP tool being called
- `parameters` (object): Parameters passed to the tool
- `result` (object, optional): Result of the tool execution
- `error` (object, optional): Error information if tool failed
- `executedAt` (datetime): When the tool was executed
- `userId` (string): ID of the user making the call

### Relationships:
- Associated with a `ChatMessage`
- Associated with a `User`

### Validation Rules:
- `toolName` must be a valid registered MCP tool
- `parameters` must match expected schema for the tool
- Only one of `result` or `error` should be present

## State Transitions

### ChatSession State Transitions:
- `inactive` → `active` when user starts new chat
- `active` → `inactive` when session times out or user closes chat
- `active` → `archived` when session is completed

### UserIntent Confidence Levels:
- `high` (>0.8): Automatically execute the corresponding action
- `medium` (0.5-0.8): Request clarification from user
- `low` (<0.5): Ask user to rephrase the request

## Indexes
- `ChatMessage.userId` for efficient user message retrieval
- `ChatMessage.sessionId` for efficient session message retrieval
- `ChatSession.userId` for efficient user session retrieval
- `ChatMessage.timestamp` for chronological ordering