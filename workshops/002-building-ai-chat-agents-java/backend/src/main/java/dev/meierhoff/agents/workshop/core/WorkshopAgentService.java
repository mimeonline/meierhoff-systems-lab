package dev.meierhoff.agents.workshop.core;

import dev.meierhoff.agents.workshop.api.ChatResponsePayload;
import dev.meierhoff.agents.workshop.debug.DebugSnapshot;
import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

/**
 * Small visible service boundary used by the HTTP layer.
 *
 * The workshop frontend only needs two capabilities: execute one chat turn and
 * inspect the collected debug information for a phase/session pair.
 */
public interface WorkshopAgentService {

    /**
     * Executes one user message in the selected phase.
     *
     * <p>The phase controls which LangChain4j features are active, for example
     * memory, tools, MCP, or retrieval.
     */
    ChatResponsePayload chat(WorkshopPhase phase, String sessionId, String message);

    /**
     * Returns the latest debug snapshot that was captured while handling the
     * phase/session conversation.
     */
    DebugSnapshot debug(WorkshopPhase phase, String sessionId);
}
