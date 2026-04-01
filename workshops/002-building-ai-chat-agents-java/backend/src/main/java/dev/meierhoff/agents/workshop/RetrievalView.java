package dev.meierhoff.agents.workshop;

public record RetrievalView(
        String source,
        double score,
        String snippet
) {
}
