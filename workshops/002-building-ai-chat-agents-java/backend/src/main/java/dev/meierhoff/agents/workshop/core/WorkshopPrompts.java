package dev.meierhoff.agents.workshop.core;

import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

/**
 * The workshop keeps prompts visible because they are part of the learning
 * story. Participants should be able to inspect how each phase reframes the
 * assistant behavior.
 */
final class WorkshopPrompts {

    private WorkshopPrompts() {
    }

    static String systemPrompt(WorkshopPhase phase) {
        return switch (phase) {
            case PHASE_1_CHAT -> """
                    You are the assistant for a Java workshop about AI agents.
                    Keep answers concise, practical, and understandable for developers.
                    Do not invent workshop-internal facts.
                    """;
            case PHASE_2_MEMORY -> """
                    You are the assistant for a Java workshop about AI agents.
                    Use the conversation memory when it helps connect turns.
                    Keep the explanation practical and brief.
                    """;
            case PHASE_3_TOOL -> """
                    You are the assistant for a Java workshop about AI agents.
                    Use local tools when the user asks for calculations or current time.
                    Briefly mention when a tool meaningfully changed the answer.
                    """;
            case PHASE_4_MCP -> """
                    You are the assistant for a Java workshop about AI agents.
                    You can access workshop files through MCP-backed tools.
                    Use MCP when the answer depends on the local workshop knowledge files.
                    Say explicitly when the answer came from an MCP tool.
                    """;
            case PHASE_5_RAG -> """
                    You are the assistant for a Java workshop about AI agents.
                    When retrieval context is provided, use it carefully and cite the file names inline.
                    If the context does not answer the question, say so instead of guessing.
                    """;
            case PHASE_6_COMPARE -> """
                    You compare different agent setups for a Java workshop.
                    Summarize what changes across plain chat, memory, tools, and RAG.
                    """;
        };
    }

    static String ragAugmentation(String userMessage, String retrievalContext) {
        return """
                Answer the user using the retrieved workshop context when it helps.
                Make the source influence visible by mentioning file names inline.

                Retrieved context:
                %s

                User question:
                %s
                """.formatted(retrievalContext, userMessage);
    }
}
