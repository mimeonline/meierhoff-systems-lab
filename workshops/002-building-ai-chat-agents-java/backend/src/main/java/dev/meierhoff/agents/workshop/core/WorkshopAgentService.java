package dev.meierhoff.agents.workshop.core;

import dev.meierhoff.agents.workshop.api.ChatResponsePayload;
import dev.meierhoff.agents.workshop.debug.DebugSnapshot;
import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

public interface WorkshopAgentService {

    ChatResponsePayload chat(WorkshopPhase phase, String sessionId, String message);

    DebugSnapshot debug(WorkshopPhase phase, String sessionId);
}
