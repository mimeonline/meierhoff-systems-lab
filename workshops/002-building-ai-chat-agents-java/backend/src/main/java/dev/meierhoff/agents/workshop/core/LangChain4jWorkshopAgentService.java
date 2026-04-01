package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.data.message.ChatMessage;
import dev.langchain4j.service.AiServices;
import dev.langchain4j.service.tool.BeforeToolExecution;
import dev.langchain4j.service.tool.ToolExecution;
import dev.meierhoff.agents.internal.debug.DebugStateStore;
import dev.meierhoff.agents.internal.debug.InvocationScope;
import dev.meierhoff.agents.internal.support.PromptFormatter;
import dev.meierhoff.agents.workshop.api.ChatResponsePayload;
import dev.meierhoff.agents.workshop.debug.ComparisonResult;
import dev.meierhoff.agents.workshop.debug.DebugSnapshot;
import dev.meierhoff.agents.workshop.debug.RetrievalView;
import dev.meierhoff.agents.workshop.debug.ToolCallView;
import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

/**
 * This is the visible LangChain4j implementation that workshop participants
 * should read.
 *
 * The didactic goal is simple:
 * participants should see how each phase is assembled,
 * which LangChain4j feature changes the system,
 * and which capabilities are active for the selected phase.
 */
public final class LangChain4jWorkshopAgentService implements WorkshopAgentService {

    private final DebugStateStore debugStateStore = new DebugStateStore();
    private final WorkshopDependencies dependencies;
    private final WorkshopTools workshopTools = new WorkshopTools();
    private final WorkshopAssistants.SingleTurnAssistant phase1Assistant;
    private final WorkshopAssistants.SessionAssistant phase2Assistant;
    private final WorkshopAssistants.SessionAssistant phase3Assistant;
    private final WorkshopAssistants.SessionAssistant phase4Assistant;
    private final WorkshopAssistants.SessionAssistant phase5Assistant;

    public LangChain4jWorkshopAgentService(WorkshopDependencies dependencies) {
        this.dependencies = dependencies;

        this.phase1Assistant = AiServices.builder(WorkshopAssistants.SingleTurnAssistant.class)
                .chatModel(dependencies.chatModel())
                .systemMessageProvider(ignored -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_1_CHAT))
                .chatRequestTransformer((request, ignored) -> capturePrompt(WorkshopPhase.PHASE_1_CHAT, request.messages(), null, request))
                .build();

        this.phase2Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
                .chatModel(dependencies.chatModel())
                .chatMemoryProvider(dependencies.memory())
                .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_2_MEMORY))
                .chatRequestTransformer((request, memoryId) -> capturePrompt(WorkshopPhase.PHASE_2_MEMORY, request.messages(), memoryId, request))
                .build();

        this.phase3Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
                .chatModel(dependencies.chatModel())
                .chatMemoryProvider(dependencies.memory())
                .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_3_TOOL))
                .tools(workshopTools)
                .beforeToolExecution(this::beforeToolExecution)
                .afterToolExecution(this::afterToolExecution)
                .chatRequestTransformer((request, memoryId) -> capturePrompt(WorkshopPhase.PHASE_3_TOOL, request.messages(), memoryId, request))
                .build();

        this.phase4Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
                .chatModel(dependencies.chatModel())
                .chatMemoryProvider(dependencies.memory())
                .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_4_MCP))
                .toolProvider(dependencies.mcpToolProvider())
                .beforeToolExecution(this::beforeToolExecution)
                .afterToolExecution(this::afterToolExecution)
                .chatRequestTransformer((request, memoryId) -> capturePrompt(WorkshopPhase.PHASE_4_MCP, request.messages(), memoryId, request))
                .build();

        this.phase5Assistant = AiServices.builder(WorkshopAssistants.SessionAssistant.class)
                .chatModel(dependencies.chatModel())
                .chatMemoryProvider(dependencies.memory())
                .systemMessageProvider(memoryId -> WorkshopPrompts.systemPrompt(WorkshopPhase.PHASE_5_RAG))
                .chatRequestTransformer((request, memoryId) -> capturePrompt(WorkshopPhase.PHASE_5_RAG, request.messages(), memoryId, request))
                .build();
    }

    @Override
    public ChatResponsePayload chat(WorkshopPhase phase, String sessionId, String message) {
        String effectiveSessionId = sessionId == null || sessionId.isBlank()
                ? UUID.randomUUID().toString()
                : sessionId;

        DebugStateStore.MutableDebugState state = debugStateStore.stateFor(phase, effectiveSessionId);
        state.startTurn();

        return switch (phase) {
            case PHASE_1_CHAT -> new ChatResponsePayload(
                    effectiveSessionId,
                    phase.apiValue(),
                    invokeWithoutMemory(phase, effectiveSessionId, message),
                    List.of()
            );
            case PHASE_2_MEMORY, PHASE_3_TOOL, PHASE_4_MCP -> new ChatResponsePayload(
                    effectiveSessionId,
                    phase.apiValue(),
                    invokeSessionAssistant(phase, effectiveSessionId, message),
                    List.of()
            );
            case PHASE_5_RAG -> new ChatResponsePayload(
                    effectiveSessionId,
                    phase.apiValue(),
                    invokeRagAssistant(effectiveSessionId, message),
                    List.of()
            );
            case PHASE_6_COMPARE -> compare(effectiveSessionId, message);
        };
    }

    @Override
    public DebugSnapshot debug(WorkshopPhase phase, String sessionId) {
        return debugStateStore.snapshot(phase, sessionId);
    }

    private ChatResponsePayload compare(String sessionId, String message) {
        List<ComparisonResult> comparisons = new ArrayList<>();
        comparisons.add(compareVariant(WorkshopPhase.PHASE_1_CHAT, sessionId, message));
        comparisons.add(compareVariant(WorkshopPhase.PHASE_2_MEMORY, sessionId, message));
        comparisons.add(compareVariant(WorkshopPhase.PHASE_3_TOOL, sessionId, message));
        comparisons.add(compareVariant(WorkshopPhase.PHASE_5_RAG, sessionId, message));

        DebugStateStore.MutableDebugState compareState = debugStateStore.stateFor(WorkshopPhase.PHASE_6_COMPARE, sessionId);
        compareState.startTurn();
        compareState.updatePrompt("Phase 6 orchestrates multiple assistant variants instead of sending one direct prompt.");
        compareState.setComparisons(comparisons);

        return new ChatResponsePayload(
                sessionId,
                WorkshopPhase.PHASE_6_COMPARE.apiValue(),
                "Comparison complete. Review the variants below to see how memory, tools, and retrieval change the answer shape.",
                comparisons
        );
    }

    private ComparisonResult compareVariant(WorkshopPhase phase, String sessionId, String message) {
        String compareSession = sessionId + "::" + phase.apiValue();
        String answer = switch (phase) {
            case PHASE_1_CHAT -> invokeWithoutMemory(phase, compareSession, message);
            case PHASE_2_MEMORY, PHASE_3_TOOL, PHASE_4_MCP -> invokeSessionAssistant(phase, compareSession, message);
            case PHASE_5_RAG -> invokeRagAssistant(compareSession, message);
            case PHASE_6_COMPARE -> throw new IllegalArgumentException("Nested compare is not supported");
        };
        return new ComparisonResult(phase.apiValue(), phase.title(), answer);
    }

    private String invokeWithoutMemory(WorkshopPhase phase, String sessionId, String message) {
        String answer = InvocationScope.with(phase, sessionId, () -> phase1Assistant.chat(message));
        debugStateStore.stateFor(phase, sessionId).replaceMemory(List.of());
        return answer;
    }

    private String invokeSessionAssistant(WorkshopPhase phase, String sessionId, String message) {
        WorkshopAssistants.SessionAssistant assistant = switch (phase) {
            case PHASE_2_MEMORY -> phase2Assistant;
            case PHASE_3_TOOL -> phase3Assistant;
            case PHASE_4_MCP -> phase4Assistant;
            default -> throw new IllegalArgumentException("Unsupported session assistant phase: " + phase);
        };

        String answer = InvocationScope.with(phase, sessionId, () -> assistant.chat(sessionId, message));
        debugStateStore.stateFor(phase, sessionId).replaceMemory(dependencies.memory().messages(sessionId));
        return answer;
    }

    private String invokeRagAssistant(String sessionId, String message) {
        List<WorkshopKnowledgeSource.RetrievedChunk> chunks = dependencies.knowledgeSource().retrieve(message, 3);
        DebugStateStore.MutableDebugState state = debugStateStore.stateFor(WorkshopPhase.PHASE_5_RAG, sessionId);

        for (WorkshopKnowledgeSource.RetrievedChunk chunk : chunks) {
            state.addRetrieval(new RetrievalView(
                    chunk.source(),
                    chunk.score(),
                    chunk.text().substring(0, Math.min(chunk.text().length(), 220))
            ));
        }

        String retrievalContext = chunks.stream()
                .map(chunk -> "[" + chunk.source() + "] " + chunk.text())
                .reduce((left, right) -> left + System.lineSeparator() + System.lineSeparator() + right)
                .orElse("No relevant workshop notes were found.");

        String augmentedMessage = WorkshopPrompts.ragAugmentation(message, retrievalContext);
        String answer = InvocationScope.with(WorkshopPhase.PHASE_5_RAG, sessionId, () -> phase5Assistant.chat(sessionId, augmentedMessage));
        state.replaceMemory(dependencies.memory().messages(sessionId));
        return answer;
    }

    /**
     * We capture the prompt for the debug panel before the request is sent to the
     * model. This is useful for learning because participants can inspect how the
     * prompt changes once memory or retrieval are added.
     */
    private dev.langchain4j.model.chat.request.ChatRequest capturePrompt(
            WorkshopPhase fallbackPhase,
            List<ChatMessage> messages,
            Object memoryId,
            dev.langchain4j.model.chat.request.ChatRequest request
    ) {
        InvocationScope.InvocationContext context = InvocationScope.current();
        WorkshopPhase phase = context != null ? context.phase() : fallbackPhase;
        String sessionId = context != null
                ? context.sessionId()
                : memoryId == null ? "single-turn" : memoryId.toString();
        debugStateStore.stateFor(phase, sessionId).updatePrompt(PromptFormatter.format(messages));
        return request;
    }

    private void beforeToolExecution(BeforeToolExecution event) {
        InvocationScope.InvocationContext context = InvocationScope.current();
        if (context == null) {
            return;
        }
        debugStateStore.stateFor(context.phase(), context.sessionId()).addToolCall(
                new ToolCallView(event.request().name(), event.request().arguments(), "pending")
        );
    }

    private void afterToolExecution(ToolExecution event) {
        InvocationScope.InvocationContext context = InvocationScope.current();
        if (context == null) {
            return;
        }
        debugStateStore.stateFor(context.phase(), context.sessionId()).completeToolCall(
                new ToolCallView(event.request().name(), event.request().arguments(), String.valueOf(event.result()))
        );
    }
}
