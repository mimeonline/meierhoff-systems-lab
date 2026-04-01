package dev.meierhoff.agents.workshop.debug;

/**
 * One tool call shown in the debug panel.
 */
public record ToolCallView(
        String toolName,
        String arguments,
        String result
) {
}
