package dev.meierhoff.agents.workshop;

public enum WorkshopPhase {
    PHASE_1_CHAT("phase-1-chat", "Phase 1 - Plain chat"),
    PHASE_2_MEMORY("phase-2-memory", "Phase 2 - Memory"),
    PHASE_3_TOOL("phase-3-tool", "Phase 3 - Tool usage"),
    PHASE_4_MCP("phase-4-mcp", "Phase 4 - MCP"),
    PHASE_5_RAG("phase-5-rag", "Phase 5 - RAG"),
    PHASE_6_COMPARE("phase-6-compare", "Phase 6 - Compare");

    private final String apiValue;
    private final String title;

    WorkshopPhase(String apiValue, String title) {
        this.apiValue = apiValue;
        this.title = title;
    }

    public String apiValue() {
        return apiValue;
    }

    public String title() {
        return title;
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
