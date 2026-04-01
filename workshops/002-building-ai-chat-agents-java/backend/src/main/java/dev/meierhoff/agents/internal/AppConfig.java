package dev.meierhoff.agents.internal;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

final class AppConfig {

    private final int port;
    private final String provider;
    private final String openAiBaseUrl;
    private final String openAiApiKey;
    private final String openAiModel;
    private final String ollamaBaseUrl;
    private final String ollamaModel;
    private final int maxMemoryMessages;
    private final Path workshopRoot;
    private final Path knowledgeDirectory;
    private final Path frontendDirectory;
    private final List<String> mcpCommand;

    private AppConfig(
            int port,
            String provider,
            String openAiBaseUrl,
            String openAiApiKey,
            String openAiModel,
            String ollamaBaseUrl,
            String ollamaModel,
            int maxMemoryMessages,
            Path workshopRoot,
            Path knowledgeDirectory,
            Path frontendDirectory,
            List<String> mcpCommand
    ) {
        this.port = port;
        this.provider = provider;
        this.openAiBaseUrl = openAiBaseUrl;
        this.openAiApiKey = openAiApiKey;
        this.openAiModel = openAiModel;
        this.ollamaBaseUrl = ollamaBaseUrl;
        this.ollamaModel = ollamaModel;
        this.maxMemoryMessages = maxMemoryMessages;
        this.workshopRoot = workshopRoot;
        this.knowledgeDirectory = knowledgeDirectory;
        this.frontendDirectory = frontendDirectory;
        this.mcpCommand = mcpCommand;
    }

    static AppConfig fromEnvironment() {
        Path workshopRoot = ProjectPaths.detectWorkshopRoot();
        Map<String, String> envFileValues = EnvFiles.load(workshopRoot);
        String provider = read(envFileValues, "WORKSHOP_MODEL_PROVIDER", "github");

        return new AppConfig(
                Integer.parseInt(read(envFileValues, "WORKSHOP_PORT", "8080")),
                provider,
                read(envFileValues, "OPENAI_BASE_URL", read(envFileValues, "GITHUB_MODELS_BASE_URL", "https://models.github.ai/inference")),
                read(envFileValues, "OPENAI_API_KEY", read(envFileValues, "GITHUB_TOKEN", "")),
                read(envFileValues, "OPENAI_MODEL", read(envFileValues, "GITHUB_MODEL", "openai/gpt-4.1-mini")),
                read(envFileValues, "OLLAMA_BASE_URL", "http://localhost:11434"),
                read(envFileValues, "OLLAMA_MODEL", "qwen2.5:7b"),
                Integer.parseInt(read(envFileValues, "WORKSHOP_MEMORY_MAX_MESSAGES", "12")),
                workshopRoot,
                workshopRoot.resolve("knowledge"),
                workshopRoot.resolve("frontend"),
                defaultMcpCommand(workshopRoot, envFileValues)
        );
    }

    private static List<String> defaultMcpCommand(Path workshopRoot, Map<String, String> envFileValues) {
        String configured = read(envFileValues, "WORKSHOP_MCP_COMMAND", "");
        if (!configured.isBlank()) {
            return List.of(configured.split("\\s+"));
        }
        return List.of(
                "npx",
                "-y",
                "@modelcontextprotocol/server-filesystem",
                workshopRoot.resolve("knowledge").toString()
        );
    }

    private static String read(Map<String, String> envFileValues, String key, String fallback) {
        String value = System.getenv(key);
        if (value == null || value.isBlank()) {
            value = envFileValues.get(key);
        }
        return value == null || value.isBlank() ? fallback : value;
    }

    int port() {
        return port;
    }

    String provider() {
        return provider;
    }

    String openAiBaseUrl() {
        return openAiBaseUrl;
    }

    String openAiApiKey() {
        return openAiApiKey;
    }

    String openAiModel() {
        return openAiModel;
    }

    String ollamaBaseUrl() {
        return ollamaBaseUrl;
    }

    String ollamaModel() {
        return ollamaModel;
    }

    int maxMemoryMessages() {
        return maxMemoryMessages;
    }

    Path workshopRoot() {
        return workshopRoot;
    }

    Path knowledgeDirectory() {
        return knowledgeDirectory;
    }

    Path frontendDirectory() {
        return frontendDirectory;
    }

    List<String> mcpCommand() {
        return mcpCommand;
    }
}
