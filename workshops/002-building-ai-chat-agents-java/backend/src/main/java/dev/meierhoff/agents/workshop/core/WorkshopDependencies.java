package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.service.tool.ToolProvider;

public record WorkshopDependencies(
        ChatModel chatModel,
        WorkshopMemory memory,
        ToolProvider mcpToolProvider,
        WorkshopKnowledgeSource knowledgeSource
) {
}
