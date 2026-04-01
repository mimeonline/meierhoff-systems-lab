package dev.meierhoff.agents.internal;

import dev.langchain4j.data.message.ChatMessage;

import java.util.List;
import java.util.stream.Collectors;

final class PromptFormatter {

    private PromptFormatter() {
    }

    static String format(List<ChatMessage> messages) {
        return messages.stream()
                .map(message -> message.type() + System.lineSeparator() + message)
                .collect(Collectors.joining(System.lineSeparator() + System.lineSeparator()));
    }
}
