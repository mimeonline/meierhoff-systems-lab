package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.memory.chat.ChatMemoryProvider;

import java.util.List;

/**
 * Visible memory abstraction used by the workshop service.
 *
 * <p>It extends LangChain4j's {@link ChatMemoryProvider} so AI services can use
 * it directly, and adds a second method that exposes the current memory window
 * in a debug-friendly format for the UI.
 */
public interface WorkshopMemory extends ChatMemoryProvider {

    /**
     * Returns the current memory contents in a simple string representation for
     * the debug panel.
     */
    List<String> messages(Object memoryId);
}
