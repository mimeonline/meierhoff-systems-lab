package dev.meierhoff.agents.internal.support;

import dev.langchain4j.data.message.ChatMessage;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Converts LangChain4j chat messages into a readable debug string for the UI.
 */
public final class PromptFormatter {

    private PromptFormatter() {
    }

    public static String format(List<ChatMessage> messages) {
        return messages.stream()
                .map(message -> message.type() + System.lineSeparator() + message)
                .collect(Collectors.joining(System.lineSeparator() + System.lineSeparator()));
    }
}
