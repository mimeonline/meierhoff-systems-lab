package dev.meierhoff.agents.workshop.api;

/**
 * Incoming payload for POST /chat.
 *
 * This record belongs to the transport layer, not to the core LangChain4j
 * learning path. It is isolated in `workshop.api` so participants can ignore it
 * if they want to focus on the agent construction itself.
 */
public record ChatRequestPayload(
        String message,
        String sessionId,
        String phase
) {
}
