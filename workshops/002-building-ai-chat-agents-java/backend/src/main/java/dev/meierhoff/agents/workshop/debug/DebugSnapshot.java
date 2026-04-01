package dev.meierhoff.agents.workshop.debug;

import java.util.List;

/**
 * Visible debug state returned by GET /debug.
 */
public record DebugSnapshot(
        String sessionId,
        String phase,
        String prompt,
        List<String> memory,
        List<ToolCallView> toolCalls,
        List<RetrievalView> retrievals,
        List<ComparisonResult> comparisons
) {
}
