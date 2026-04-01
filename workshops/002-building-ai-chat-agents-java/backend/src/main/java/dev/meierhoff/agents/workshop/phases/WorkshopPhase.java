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
                    "internal/memory/InspectableChatMemoryStore"
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
                    "internal/mcp/McpSupport",
                    "internal/bootstrap/WorkshopRuntimeFactory"
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
                    "internal/rag/KnowledgeBase",
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

    /**
     * Stable value used by the frontend and REST API.
     */
    public String apiValue() {
        return apiValue;
    }

    /**
     * Human-readable title used in the UI and workshop material.
     */
    public String title() {
        return title;
    }

    /**
     * Whether this phase keeps conversational state across turns.
     */
    public boolean usesMemory() {
        return usesMemory;
    }

    /**
     * Whether this phase exposes local Java methods as tools.
     */
    public boolean usesDirectTools() {
        return usesDirectTools;
    }

    /**
     * Whether this phase reaches tools through MCP instead of direct methods.
     */
    public boolean usesMcp() {
        return usesMcp;
    }

    /**
     * Whether this phase augments the prompt with retrieved knowledge chunks.
     */
    public boolean usesRag() {
        return usesRag;
    }

    /**
     * Phase 6 does not run one assistant directly. It compares several setups.
     */
    public boolean isComparisonPhase() {
        return this == PHASE_6_COMPARE;
    }

    /**
     * Returns the most useful files to read for this phase.
     */
    public List<String> relevantFiles() {
        return relevantFiles;
    }

    /**
     * Turns the file list into one compact suggested reading path.
     */
    public String readingGuide() {
        return String.join(" -> ", relevantFiles);
    }

    /**
     * Returns the workshop concepts that are active in this phase.
     */
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

    /**
     * Resolves a phase name from the REST API.
     *
     * <p>An empty value falls back to phase 1 so the UI can start with the
     * simplest setup by default.
     */
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
