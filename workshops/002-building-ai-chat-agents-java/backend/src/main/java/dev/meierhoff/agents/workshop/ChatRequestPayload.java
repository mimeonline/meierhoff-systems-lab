package dev.meierhoff.agents.workshop;

public record ChatRequestPayload(
        String message,
        String sessionId,
        String phase
) {
}
