package dev.meierhoff.agents.workshop.core;

import java.util.List;

/**
 * Visible abstraction for retrieval.
 *
 * <p>Participants should understand that the agent asks a knowledge source for
 * matching chunks. They do not need to know whether the hidden implementation
 * uses an in-memory store, a database, or another vector backend.
 */
public interface WorkshopKnowledgeSource {

    /**
     * Retrieves the most relevant knowledge chunks for a user query.
     */
    List<RetrievedChunk> retrieve(String query, int maxResults);

    /**
     * Simple visible view of one retrieval result.
     */
    record RetrievedChunk(String source, double score, String text) {
    }
}
