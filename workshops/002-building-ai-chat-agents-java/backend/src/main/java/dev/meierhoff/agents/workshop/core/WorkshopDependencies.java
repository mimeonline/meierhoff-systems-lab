package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.service.tool.ToolProvider;

/**
 * Visible bundle of the runtime building blocks that the workshop code needs.
 *
 * <p>The point of this record is didactic: the learning layer can talk about a
 * chat model, memory, MCP tools, and a knowledge source without exposing how
 * those pieces are instantiated internally.
 */
public record WorkshopDependencies(
        ChatModel chatModel,
        WorkshopMemory memory,
        ToolProvider mcpToolProvider,
        WorkshopKnowledgeSource knowledgeSource
) {
}
