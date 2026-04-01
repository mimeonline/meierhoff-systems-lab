package dev.meierhoff.agents.workshop;

public interface WorkshopAgentService {

    ChatResponsePayload chat(WorkshopPhase phase, String sessionId, String message);

    DebugSnapshot debug(WorkshopPhase phase, String sessionId);
}
