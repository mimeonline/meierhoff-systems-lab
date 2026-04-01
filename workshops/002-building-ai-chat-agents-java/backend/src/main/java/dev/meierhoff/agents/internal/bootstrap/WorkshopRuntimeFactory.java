package dev.meierhoff.agents.internal.bootstrap;

import dev.meierhoff.agents.internal.config.AppConfig;
import dev.meierhoff.agents.internal.mcp.McpSupport;
import dev.meierhoff.agents.internal.memory.InspectableChatMemoryStore;
import dev.meierhoff.agents.internal.model.ModelFactory;
import dev.meierhoff.agents.internal.rag.KnowledgeBase;
import dev.meierhoff.agents.workshop.core.WorkshopDependencies;

/**
 * Builds the runtime dependencies that are useful but not educational for the
 * workshop audience: provider selection, memory implementation choice, MCP
 * client setup, and retrieval index initialization.
 */
public final class WorkshopRuntimeFactory {

    private WorkshopRuntimeFactory() {
    }

    /**
     * Assembles the hidden runtime implementations behind the visible workshop
     * abstractions.
     */
    public static WorkshopDependencies create(AppConfig config) {
        return new WorkshopDependencies(
                ModelFactory.createChatModel(config),
                new InspectableChatMemoryStore(config.maxMemoryMessages()),
                McpSupport.createToolProvider(config),
                KnowledgeBase.load(config.knowledgeDirectory())
        );
    }
}
