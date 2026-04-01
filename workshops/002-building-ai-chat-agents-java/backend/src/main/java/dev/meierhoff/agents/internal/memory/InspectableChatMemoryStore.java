package dev.meierhoff.agents.internal.memory;

import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;
import dev.meierhoff.agents.workshop.core.WorkshopMemory;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Chat memory implementation used by the workshop runtime.
 *
 * It deliberately exposes a formatted debug view so the frontend can show what
 * the memory window currently contains.
 */
public final class InspectableChatMemoryStore implements WorkshopMemory {

    private final int maxMessages;
    private final Map<Object, ChatMemory> memories = new ConcurrentHashMap<>();

    public InspectableChatMemoryStore(int maxMessages) {
        this.maxMessages = maxMessages;
    }

    @Override
    public ChatMemory get(Object memoryId) {
        return memories.computeIfAbsent(memoryId, ignored ->
                MessageWindowChatMemory.builder().maxMessages(maxMessages).build());
    }

    public List<String> messages(Object memoryId) {
        ChatMemory memory = memories.get(memoryId);
        if (memory == null) {
            return List.of();
        }
        return memory.messages().stream()
                .map(this::formatMessage)
                .toList();
    }

    private String formatMessage(ChatMessage message) {
        return message.type() + ": " + message.toString();
    }
}
