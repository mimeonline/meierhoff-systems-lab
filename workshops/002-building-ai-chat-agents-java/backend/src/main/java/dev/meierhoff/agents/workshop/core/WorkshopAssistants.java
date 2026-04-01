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

    interface SingleTurnAssistant {
        String chat(@UserMessage String userMessage);
    }

    interface SessionAssistant {
        String chat(@MemoryId String sessionId, @UserMessage String userMessage);
    }
}
