package dev.meierhoff.agents.internal.http;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;
import dev.meierhoff.agents.internal.config.AppConfig;
import dev.meierhoff.agents.workshop.api.ChatRequestPayload;
import dev.meierhoff.agents.workshop.api.ChatResponsePayload;
import dev.meierhoff.agents.workshop.core.WorkshopAgentService;
import dev.meierhoff.agents.workshop.debug.DebugSnapshot;
import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

import java.io.IOException;
import java.net.InetSocketAddress;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

/**
 * Tiny HTTP adapter for the workshop UI.
 *
 * We keep request parsing, static file serving, and JSON handling here so that
 * the visible workshop package can focus on agent composition only.
 */
public final class WorkshopHttpServer {

    private final AppConfig config;
    private final WorkshopAgentService service;
    private final JsonSupport jsonSupport = new JsonSupport();

    public WorkshopHttpServer(AppConfig config, WorkshopAgentService service) {
        this.config = config;
        this.service = service;
    }

    /**
     * Starts the embedded HTTP server and registers the workshop endpoints.
     */
    public void start() throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(config.port()), 0);
        server.createContext("/chat", new ChatHandler());
        server.createContext("/debug", new DebugHandler());
        server.createContext("/", new StaticHandler(config.frontendDirectory()));
        server.start();
        System.out.printf("Workshop server started on http://localhost:%d%n", config.port());
    }

    private final class ChatHandler implements HttpHandler {
        @Override
        /**
         * Handles one `POST /chat` request from the frontend.
         */
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
        /**
         * Handles `GET /debug` and returns the latest captured debug snapshot.
         */
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
        /**
         * Serves the built frontend files directly from the local `frontend/`
         * directory.
         */
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

        /**
         * Resolves a browser path to a file below the built frontend directory.
         */
        private Path resolvePath(String requestPath) {
            String normalized = requestPath.equals("/") ? "index.html" : requestPath.substring(1);
            return frontendDirectory.resolve(normalized).normalize();
        }

        /**
         * Minimal content-type mapping for the workshop frontend assets.
         */
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

    /**
     * Allows the locally served frontend to call the API during development.
     */
    private void addCorsHeaders(HttpExchange exchange) {
        exchange.getResponseHeaders().add("Access-Control-Allow-Origin", "*");
        exchange.getResponseHeaders().add("Access-Control-Allow-Headers", "Content-Type");
        exchange.getResponseHeaders().add("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
    }

    /**
     * Writes a JSON response and closes the exchange.
     */
    private void writeJson(HttpExchange exchange, int status, Object body) throws IOException {
        byte[] bytes = jsonSupport.writeBytes(body);
        exchange.getResponseHeaders().add("Content-Type", "application/json; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.close();
    }

    /**
     * Writes a plain-text response and closes the exchange.
     */
    private void writeText(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().add("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        exchange.getResponseBody().write(bytes);
        exchange.close();
    }

    private record Query(Map<String, String> values) {

        /**
         * Parses the URI query string into a simple key/value map.
         */
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

        /**
         * Returns one query parameter value or {@code null}.
         */
        String value(String key) {
            return values.get(key);
        }

        /**
         * URL-decodes one query-string component.
         */
        private static String decode(String value) {
            return java.net.URLDecoder.decode(value, StandardCharsets.UTF_8);
        }
    }
}
