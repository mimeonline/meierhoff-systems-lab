package dev.meierhoff.agents.workshop.phases;

import java.util.List;

/**
 * Visible map of the workshop progression.
 *
 * Participants should be able to read this enum and see which capability is
 * active in each phase without digging through infrastructure code.
 */
public enum WorkshopPhase {
    PHASE_1_CHAT(
            "phase-1-chat",
            "Phase 1 - Plain chat",
            false,
            false,
            false,
            false,
            List.of(
                    "workshop/core/LangChain4jWorkshopAgentService",
                    "workshop/core/WorkshopAssistants",
                    "workshop/core/WorkshopPrompts"
            )
    ),
    PHASE_2_MEMORY(
            "phase-2-memory",
            "Phase 2 - Memory",
            true,
            false,
            false,
            false,
            List.of(
                    "workshop/core/LangChain4jWorkshopAgentService",
                    "workshop/core/WorkshopAssistants",
                    "internal/InspectableChatMemoryStore"
            )
    ),
    PHASE_3_TOOL(
            "phase-3-tool",
            "Phase 3 - Tool usage",
            true,
            true,
            false,
            false,
            List.of(
                    "workshop/core/LangChain4jWorkshopAgentService",
                    "workshop/core/WorkshopTools",
                    "workshop/debug/ToolCallView"
            )
    ),
    PHASE_4_MCP(
            "phase-4-mcp",
            "Phase 4 - MCP",
            true,
            false,
            true,
            false,
            List.of(
                    "workshop/core/LangChain4jWorkshopAgentService",
                    "internal/McpSupport",
                    "internal/WorkshopRuntimeFactory"
            )
    ),
    PHASE_5_RAG(
            "phase-5-rag",
            "Phase 5 - RAG",
            true,
            false,
            false,
            true,
            List.of(
                    "workshop/core/LangChain4jWorkshopAgentService",
                    "workshop/core/WorkshopPrompts",
                    "internal/KnowledgeBase",
                    "workshop/debug/RetrievalView"
            )
    ),
    PHASE_6_COMPARE(
            "phase-6-compare",
            "Phase 6 - Compare",
            false,
            false,
            false,
            false,
            List.of(
                    "workshop/core/LangChain4jWorkshopAgentService",
                    "workshop/debug/ComparisonResult"
            )
    );

    private final String apiValue;
    private final String title;
    private final boolean usesMemory;
    private final boolean usesDirectTools;
    private final boolean usesMcp;
    private final boolean usesRag;
    private final List<String> relevantFiles;

    WorkshopPhase(
            String apiValue,
            String title,
            boolean usesMemory,
            boolean usesDirectTools,
            boolean usesMcp,
            boolean usesRag,
            List<String> relevantFiles
    ) {
        this.apiValue = apiValue;
        this.title = title;
        this.usesMemory = usesMemory;
        this.usesDirectTools = usesDirectTools;
        this.usesMcp = usesMcp;
        this.usesRag = usesRag;
        this.relevantFiles = List.copyOf(relevantFiles);
    }

    public String apiValue() {
        return apiValue;
    }

    public String title() {
        return title;
    }

    public boolean usesMemory() {
        return usesMemory;
    }

    public boolean usesDirectTools() {
        return usesDirectTools;
    }

    public boolean usesMcp() {
        return usesMcp;
    }

    public boolean usesRag() {
        return usesRag;
    }

    public boolean isComparisonPhase() {
        return this == PHASE_6_COMPARE;
    }

    public List<String> relevantFiles() {
        return relevantFiles;
    }

    public String readingGuide() {
        return String.join(" -> ", relevantFiles);
    }

    public List<String> activeConcepts() {
        List<String> concepts = new java.util.ArrayList<>();
        concepts.add("chat");
        if (usesMemory) {
            concepts.add("memory");
        }
        if (usesDirectTools) {
            concepts.add("tool");
        }
        if (usesMcp) {
            concepts.add("mcp");
        }
        if (usesRag) {
            concepts.add("rag");
        }
        if (isComparisonPhase()) {
            concepts.add("comparison");
        }
        return List.copyOf(concepts);
    }

    public static WorkshopPhase fromApiValue(String value) {
        if (value == null || value.isBlank()) {
            return PHASE_1_CHAT;
        }
        for (WorkshopPhase phase : values()) {
            if (phase.apiValue.equalsIgnoreCase(value)) {
                return phase;
            }
        }
        throw new IllegalArgumentException("Unknown phase: " + value);
    }
}
