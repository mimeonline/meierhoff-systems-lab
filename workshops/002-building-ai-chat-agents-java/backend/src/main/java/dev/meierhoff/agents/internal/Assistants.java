package dev.meierhoff.agents.internal;

import dev.langchain4j.service.MemoryId;
import dev.langchain4j.service.UserMessage;

final class Assistants {

    private Assistants() {
    }

    interface SingleTurnAssistant {
        String chat(@UserMessage String userMessage);
    }

    interface SessionAssistant {
        String chat(@MemoryId String sessionId, @UserMessage String userMessage);
    }
}
