package dev.meierhoff.agents.workshop;

public record ToolCallView(
        String toolName,
        String arguments,
        String result
) {
}
