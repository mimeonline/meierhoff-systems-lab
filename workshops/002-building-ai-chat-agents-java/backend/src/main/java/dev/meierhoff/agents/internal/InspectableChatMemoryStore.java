package dev.meierhoff.agents.internal;

import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.memory.ChatMemory;
import dev.langchain4j.memory.chat.ChatMemoryProvider;
import dev.langchain4j.memory.chat.MessageWindowChatMemory;

import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

final class InspectableChatMemoryStore implements ChatMemoryProvider {

    private final int maxMessages;
    private final Map<Object, ChatMemory> memories = new ConcurrentHashMap<>();

    InspectableChatMemoryStore(int maxMessages) {
        this.maxMessages = maxMessages;
    }

    @Override
    public ChatMemory get(Object memoryId) {
        return memories.computeIfAbsent(memoryId, ignored ->
                MessageWindowChatMemory.builder().maxMessages(maxMessages).build());
    }

    List<String> messages(Object memoryId) {
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
