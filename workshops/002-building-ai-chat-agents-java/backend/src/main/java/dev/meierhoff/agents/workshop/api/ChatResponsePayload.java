package dev.meierhoff.agents.workshop.api;

import dev.meierhoff.agents.workshop.debug.ComparisonResult;

import java.util.List;

/**
 * Outgoing payload for POST /chat.
 */
public record ChatResponsePayload(
        String sessionId,
        String phase,
        String answer,
        List<ComparisonResult> comparisons
) {
}
