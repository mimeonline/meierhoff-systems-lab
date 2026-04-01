package dev.meierhoff.agents.internal;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import dev.meierhoff.agents.workshop.ChatRequestPayload;
import dev.meierhoff.agents.workshop.ChatResponsePayload;
import dev.meierhoff.agents.workshop.DebugSnapshot;
import dev.meierhoff.agents.workshop.WorkshopAgentService;
import dev.meierhoff.agents.workshop.WorkshopPhase;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

final class WorkshopHttpServer {

    private final AppConfig config;
    private final WorkshopAgentService service;
    private final JsonSupport jsonSupport = new JsonSupport();

    WorkshopHttpServer(AppConfig config, WorkshopAgentService service) {
        this.config = config;
        this.service = service;
    }

    void start() throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(config.port()), 0);
        server.createContext("/chat", new ChatHandler());
        server.createContext("/debug", new DebugHandler());
        server.createContext("/", new StaticHandler(config.frontendDirectory()));
        server.start();
        System.out.printf("Workshop server started on http://localhost:%d%n", config.port());
    }

    private final class ChatHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if ("OPTIONS".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(204, -1);
                return;
            }
            if (!"POST".equalsIgnoreCase(exchange.getRequestMethod())) {
                writeJson(exchange, 405, Map.of("error", "Use POST /chat"));
                return;
            }

            try {
                ChatRequestPayload payload = jsonSupport.readChatRequest(exchange.getRequestBody());
                if (payload.message() == null || payload.message().isBlank()) {
                    writeJson(exchange, 400, Map.of("error", "Field 'message' is required"));
                    return;
                }

                WorkshopPhase phase = WorkshopPhase.fromApiValue(payload.phase());
                ChatResponsePayload response = service.chat(phase, payload.sessionId(), payload.message());
                writeJson(exchange, 200, response);
            } catch (Exception exception) {
                writeJson(exchange, 500, Map.of("error", exception.getMessage()));
            }
        }
    }

    private final class DebugHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            addCorsHeaders(exchange);
            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                writeJson(exchange, 405, Map.of("error", "Use GET /debug"));
                return;
            }

            try {
                Query query = Query.parse(exchange.getRequestURI());
                String sessionId = query.value("sessionId");
                if (sessionId == null || sessionId.isBlank()) {
                    writeJson(exchange, 400, Map.of("error", "Query parameter 'sessionId' is required"));
                    return;
                }

                WorkshopPhase phase = WorkshopPhase.fromApiValue(query.value("phase"));
                DebugSnapshot debug = service.debug(phase, sessionId);
                writeJson(exchange, 200, debug);
            } catch (Exception exception) {
                writeJson(exchange, 500, Map.of("error", exception.getMessage()));
            }
        }
    }

    private final class StaticHandler implements HttpHandler {
        private final Path frontendDirectory;

        private StaticHandler(Path frontendDirectory) {
            this.frontendDirectory = frontendDirectory;
        }

        @Override
        public void handle(HttpExchange exchange) throws IOException {
            if (!"GET".equalsIgnoreCase(exchange.getRequestMethod())) {
                exchange.sendResponseHeaders(405, -1);
                return;
            }

            Path target = resolvePath(exchange.getRequestURI().getPath());
            if (!Files.exists(target) || Files.isDirectory(target)) {
                target = frontendDirectory.resolve("index.html");
            }
            if (!Files.exists(target)) {
                writeText(exchange, 404, "Frontend build not found. Run the frontend build first.");
                return;
            }

            byte[] body = Files.readAllBytes(target);
            exchange.getResponseHeaders().add("Content-Type", contentType(target));
            exchange.sendResponseHeaders(200, body.length);
            exchange.getResponseBody().write(body);
            exchange.close();
        }

        private Path resolvePath(String requestPath) {
            String normalized = requestPath.equals("/") ? "index.html" : requestPath.substring(1);
            return frontendDirectory.resolve(normalized).normalize();
        }

        private String contentType(Path path) {
            String name = path.getFileName().toString();
            if (name.endsWith(".html")) {
                return "text/html; charset=utf-8";
            }
            if (name.endsWith(".js")) {
                return "text/javascript; charset=utf-8";
            }
            if (name.endsWith(".css")) {
                return "text/css; charset=utf-8";
            }
            return "text/plain; charset=utf-8";
        }
    }

    private void addCorsHeaders(HttpExchange exchange) {
        exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type");
        exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
    }

    private void writeJson(HttpExchange exchange, int status, Object body) throws IOException {
        byte[] bytes = jsonSupport.writeBytes(body);
        exchange.getResponseHeaders().add("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.close();
    }

    private void writeText(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.close();
    }

    private record Query(Map<String, String> values) {

        static Query parse(URI uri) {
            if (uri.getRawQuery() == null || uri.getRawQuery().isBlank()) {
                return new Query(Map.of());
            }
            return new Query(
                    java.util.Arrays.stream(uri.getRawQuery().split("&"))
                            .map(entry -> entry.split("=", 2))
                            .collect(java.util.stream.Collectors.toMap(
                                    pair -> decode(pair[0]),
                                    pair -> pair.length > 1 ? decode(pair[1]) : ""
                            ))
            );
        }

        String value(String key) {
            return values.get(key);
        }

        private static String decode(String value) {
            return java.net.URLDecoder.decode(value, StandardCharsets.UTF_8);
        }
    }
}
