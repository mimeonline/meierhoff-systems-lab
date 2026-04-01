package dev.meierhoff.agents.internal.mcp;

import dev.langchain4j.mcp.McpToolProvider;
import dev.langchain4j.mcp.client.DefaultMcpClient;
import dev.langchain4j.mcp.client.McpClient;
import dev.langchain4j.mcp.client.transport.stdio.StdioMcpTransport;
import dev.meierhoff.agents.internal.config.AppConfig;

/**
 * Builds the MCP client used by the workshop.
 *
 * The visible workshop layer only needs a ready-to-use {@link McpToolProvider}.
 * Transport details stay hidden here.
 */
public final class McpSupport {

    private McpSupport() {
    }

    public static McpToolProvider createToolProvider(AppConfig config) {
        StdioMcpTransport transport = StdioMcpTransport.builder()
                .command(config.mcpCommand())
                .build();

        McpClient client = DefaultMcpClient.builder()
                .key("workshop-filesystem")
                .transport(transport)
                .build();

        return McpToolProvider.builder()
                .mcpClients(client)
                .build();
    }
}
