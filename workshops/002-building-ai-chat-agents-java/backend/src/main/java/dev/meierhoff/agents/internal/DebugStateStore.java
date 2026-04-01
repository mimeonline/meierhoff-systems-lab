package dev.meierhoff.agents.internal;

import dev.meierhoff.agents.workshop.ComparisonResult;
import dev.meierhoff.agents.workshop.DebugSnapshot;
import dev.meierhoff.agents.workshop.RetrievalView;
import dev.meierhoff.agents.workshop.ToolCallView;
import dev.meierhoff.agents.workshop.WorkshopPhase;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

final class DebugStateStore {

    private final Map<String, MutableDebugState> states = new ConcurrentHashMap<>();

    MutableDebugState stateFor(WorkshopPhase phase, String sessionId) {
        return states.computeIfAbsent(key(phase, sessionId), ignored -> new MutableDebugState(sessionId, phase.apiValue()));
    }

    DebugSnapshot snapshot(WorkshopPhase phase, String sessionId) {
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

    private String key(WorkshopPhase phase, String sessionId) {
        return phase.apiValue() + "::" + sessionId;
    }

    static final class MutableDebugState {
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

        synchronized void startTurn() {
            prompt = "";
            toolCalls.clear();
            retrievals.clear();
            comparisons.clear();
        }

        synchronized void updatePrompt(String prompt) {
            this.prompt = prompt;
        }

        synchronized void replaceMemory(List<String> entries) {
            memory.clear();
            memory.addAll(entries);
        }

        synchronized void addToolCall(ToolCallView toolCallView) {
            toolCalls.add(toolCallView);
        }

        synchronized void completeToolCall(ToolCallView toolCallView) {
            for (int index = toolCalls.size() - 1; index >= 0; index--) {
                ToolCallView current = toolCalls.get(index);
                if (current.toolName().equals(toolCallView.toolName()) && "pending".equals(current.result())) {
                    toolCalls.set(index, toolCallView);
                    return;
                }
            }
            toolCalls.add(toolCallView);
        }

        synchronized void addRetrieval(RetrievalView retrievalView) {
            retrievals.add(retrievalView);
        }

        synchronized void setComparisons(List<ComparisonResult> comparisonResults) {
            comparisons.clear();
            comparisons.addAll(comparisonResults);
        }
    }
}
