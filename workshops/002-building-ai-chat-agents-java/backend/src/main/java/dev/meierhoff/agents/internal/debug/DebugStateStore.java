package dev.meierhoff.agents.internal.debug;

import dev.meierhoff.agents.workshop.debug.ComparisonResult;
import dev.meierhoff.agents.workshop.debug.DebugSnapshot;
import dev.meierhoff.agents.workshop.debug.RetrievalView;
import dev.meierhoff.agents.workshop.debug.ToolCallView;
import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * Stores the debug information that powers the workshop inspector UI.
 *
 * This is intentionally hidden from the visible workshop package because it is
 * support infrastructure, not part of the LangChain4j concepts being taught.
 */
public final class DebugStateStore {

    private final Map<String, MutableDebugState> states = new ConcurrentHashMap<>();

    /**
     * Returns the mutable debug state bucket for one phase/session pair,
     * creating it on first access.
     */
    public MutableDebugState stateFor(WorkshopPhase phase, String sessionId) {
        return states.computeIfAbsent(key(phase, sessionId), ignored -> new MutableDebugState(sessionId, phase.apiValue()));
    }

    /**
     * Creates an immutable snapshot that is safe to return through the REST API.
     */
    public DebugSnapshot snapshot(WorkshopPhase phase, String sessionId) {
        MutableDebugState state = stateFor(phase, sessionId);
        return new DebugSnapshot(
                state.sessionId,
                state.phase,
                state.prompt,
                List.copyOf(state.memory),
                List.copyOf(state.toolCalls),
                List.copyOf(state.retrievals),
                List.copyOf(state.comparisons)
        );
    }

    /**
     * Combines phase and session into one stable storage key.
     */
    private String key(WorkshopPhase phase, String sessionId) {
        return phase.apiValue() + "::" + sessionId;
    }

    public static final class MutableDebugState {
        private final String sessionId;
        private final String phase;
        private volatile String prompt = "";
        private final List<String> memory = new ArrayList<>();
        private final List<ToolCallView> toolCalls = new ArrayList<>();
        private final List<RetrievalView> retrievals = new ArrayList<>();
        private final List<ComparisonResult> comparisons = new ArrayList<>();

        MutableDebugState(String sessionId, String phase) {
            this.sessionId = sessionId;
            this.phase = phase;
        }

        /**
         * Clears per-turn data before a new request is processed.
         *
         * <p>The memory list is intentionally not cleared because chat memory is
         * conversational state, not transient turn state.
         */
        public synchronized void startTurn() {
            prompt = "";
            toolCalls.clear();
            retrievals.clear();
            comparisons.clear();
        }

        /**
         * Stores the latest prompt text shown in the debug panel.
         */
        public synchronized void updatePrompt(String prompt) {
            this.prompt = prompt;
        }

        /**
         * Replaces the visible memory snapshot after a model call completes.
         */
        public synchronized void replaceMemory(List<String> entries) {
            memory.clear();
            memory.addAll(entries);
        }

        /**
         * Adds a newly started tool call in pending state.
         */
        public synchronized void addToolCall(ToolCallView toolCallView) {
            toolCalls.add(toolCallView);
        }

        /**
         * Replaces the most recent pending tool call with its finished result.
         */
        public synchronized void completeToolCall(ToolCallView toolCallView) {
            for (int index = toolCalls.size() - 1; index >= 0; index--) {
                ToolCallView current = toolCalls.get(index);
                if (current.toolName().equals(toolCallView.toolName()) && "pending".equals(current.result())) {
                    toolCalls.set(index, toolCallView);
                    return;
                }
            }
            toolCalls.add(toolCallView);
        }

        /**
         * Appends one retrieved knowledge chunk to the debug view.
         */
        public synchronized void addRetrieval(RetrievalView retrievalView) {
            retrievals.add(retrievalView);
        }

        /**
         * Stores the phase comparison results produced by phase 6.
         */
        public synchronized void setComparisons(List<ComparisonResult> comparisonResults) {
            comparisons.clear();
            comparisons.addAll(comparisonResults);
        }
    }
}
