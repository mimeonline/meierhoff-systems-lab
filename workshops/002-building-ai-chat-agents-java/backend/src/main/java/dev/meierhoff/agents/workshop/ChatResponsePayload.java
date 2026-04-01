package dev.meierhoff.agents.workshop;

import java.util.List;

public record ChatResponsePayload(
        String sessionId,
        String phase,
        String answer,
        List<ComparisonResult> comparisons
) {
}
