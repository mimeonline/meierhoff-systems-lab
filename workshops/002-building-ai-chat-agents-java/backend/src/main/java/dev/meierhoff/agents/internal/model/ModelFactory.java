package dev.meierhoff.agents.internal.model;

import dev.langchain4j.model.chat.ChatModel;
import dev.langchain4j.model.ollama.OllamaChatModel;
import dev.langchain4j.model.openai.OpenAiChatModel;
import dev.meierhoff.agents.internal.config.AppConfig;

/**
 * Hides provider-specific model construction.
 *
 * Workshop participants should see how a ChatModel is used, not how each vendor
 * SDK is configured.
 */
public final class ModelFactory {

    private ModelFactory() {
    }

    public static ChatModel createChatModel(AppConfig config) {
        return switch (config.provider().toLowerCase()) {
            case "ollama" -> OllamaChatModel.builder()
                    .baseUrl(config.ollamaBaseUrl())
                    .modelName(config.ollamaModel())
                    .build();
            case "github", "openai" -> {
                if (config.openAiApiKey().isBlank()) {
                    throw new IllegalStateException("OPENAI_API_KEY or GITHUB_TOKEN must be set for provider " + config.provider());
                }
                yield OpenAiChatModel.builder()
                        .baseUrl(config.openAiBaseUrl())
                        .apiKey(config.openAiApiKey())
                        .modelName(config.openAiModel())
                        .build();
            }
            default -> throw new IllegalArgumentException("Unsupported model provider: " + config.provider());
        };
    }
}
