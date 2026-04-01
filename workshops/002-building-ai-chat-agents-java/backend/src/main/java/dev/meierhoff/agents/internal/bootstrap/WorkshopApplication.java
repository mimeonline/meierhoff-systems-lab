package dev.meierhoff.agents.internal.bootstrap;

import dev.meierhoff.agents.internal.config.AppConfig;
import dev.meierhoff.agents.internal.http.WorkshopHttpServer;
import dev.meierhoff.agents.workshop.core.LangChain4jWorkshopAgentService;

/**
 * Minimal application entry point for the workshop backend.
 *
 * The learning-relevant LangChain4j setup lives in {@code workshop/*}. This
 * class only boots configuration, infrastructure dependencies, and the HTTP
 * server.
 */
public final class WorkshopApplication {

    private WorkshopApplication() {
    }

    /**
     * Boot sequence for the backend process.
     *
     * <p>It loads config, assembles hidden infrastructure dependencies, creates
     * the visible workshop service, and finally starts the HTTP server.
     */
    public static void main(String[] args) throws Exception {
        AppConfig config = AppConfig.fromEnvironment();
        LangChain4jWorkshopAgentService service = new LangChain4jWorkshopAgentService(WorkshopRuntimeFactory.create(config));
        WorkshopHttpServer server = new WorkshopHttpServer(config, service);
        server.start();
    }
}
