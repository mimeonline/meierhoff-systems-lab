package dev.meierhoff.agents.internal;

import dev.langchain4j.mcp.McpToolProvider;
import dev.langchain4j.mcp.client.DefaultMcpClient;
import dev.langchain4j.mcp.client.McpClient;
import dev.langchain4j.mcp.client.transport.stdio.StdioMcpTransport;

final class McpSupport {

    private McpSupport() {
    }

    static McpToolProvider createToolProvider(AppConfig config) {
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
