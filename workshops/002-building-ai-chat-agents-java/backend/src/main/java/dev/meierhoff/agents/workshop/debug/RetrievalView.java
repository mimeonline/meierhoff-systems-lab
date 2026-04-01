package dev.meierhoff.agents.workshop.debug;

/**
 * One retrieved chunk shown in the debug panel.
 */
public record RetrievalView(
        String source,
        double score,
        String snippet
) {
}
