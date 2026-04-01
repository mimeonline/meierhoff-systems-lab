package dev.meierhoff.agents.workshop.core;

import java.util.List;

public interface WorkshopKnowledgeSource {

    List<RetrievedChunk> retrieve(String query, int maxResults);

    record RetrievedChunk(String source, double score, String text) {
    }
}
