package dev.meierhoff.agents.workshop;

import java.util.List;

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
