package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.service.MemoryId;
import dev.langchain4j.service.UserMessage;

/**
 * These small interfaces are the heart of the LangChain4j teaching example.
 *
 * LangChain4j turns them into runnable AI services. Participants can read these
 * signatures and immediately see the difference between a single-turn assistant
 * and a session-aware assistant with memory.
 */
final class WorkshopAssistants {

    private WorkshopAssistants() {
    }

    /**
     * Single-turn assistant for phase 1.
     *
     * <p>No memory identifier means every call is isolated from previous turns.
     */
    interface SingleTurnAssistant {
        String chat(@UserMessage String userMessage);
    }

    /**
     * Session-aware assistant for phases that keep memory.
     *
     * <p>The {@link MemoryId} tells LangChain4j which chat memory instance should
     * be reused for this conversation.
     */
    interface SessionAssistant {
        String chat(@MemoryId String sessionId, @UserMessage String userMessage);
    }
}
