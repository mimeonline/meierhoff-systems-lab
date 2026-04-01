package dev.meierhoff.agents.internal;

public final class WorkshopApplication {

    private WorkshopApplication() {
    }

    public static void main(String[] args) throws Exception {
        AppConfig config = AppConfig.fromEnvironment();
        LangChainWorkshopAgentService service = new LangChainWorkshopAgentService(config);
        WorkshopHttpServer server = new WorkshopHttpServer(config, service);
        server.start();
    }
}
