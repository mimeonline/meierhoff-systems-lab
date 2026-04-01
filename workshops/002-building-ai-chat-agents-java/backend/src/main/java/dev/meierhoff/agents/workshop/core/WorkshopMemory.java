package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.memory.chat.ChatMemoryProvider;

import java.util.List;

public interface WorkshopMemory extends ChatMemoryProvider {

    List<String> messages(Object memoryId);
}
