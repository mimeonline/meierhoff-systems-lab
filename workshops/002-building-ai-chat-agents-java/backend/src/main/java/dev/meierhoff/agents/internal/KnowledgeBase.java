package dev.meierhoff.agents.internal;

import dev.langchain4j.data.embedding.Embedding;
import dev.langchain4j.model.embedding.EmbeddingModel;
import dev.langchain4j.model.embedding.onnx.allminilml6v2q.AllMiniLmL6V2QuantizedEmbeddingModel;
import dev.langchain4j.store.embedding.EmbeddingMatch;
import dev.langchain4j.store.embedding.EmbeddingSearchRequest;
import dev.langchain4j.store.embedding.EmbeddingSearchResult;
import dev.langchain4j.store.embedding.inmemory.InMemoryEmbeddingStore;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Locale;

final class KnowledgeBase {

    private final EmbeddingModel embeddingModel;
    private final InMemoryEmbeddingStore<KnowledgeChunk> store;

    private KnowledgeBase(EmbeddingModel embeddingModel, InMemoryEmbeddingStore<KnowledgeChunk> store) {
        this.embeddingModel = embeddingModel;
        this.store = store;
    }

    static KnowledgeBase load(Path knowledgeDirectory) {
        try {
            EmbeddingModel embeddingModel = new AllMiniLmL6V2QuantizedEmbeddingModel();
            InMemoryEmbeddingStore<KnowledgeChunk> store = new InMemoryEmbeddingStore<>();

            List<Path> files = Files.list(knowledgeDirectory)
                    .filter(path -> path.getFileName().toString().endsWith(".md"))
                    .sorted(Comparator.comparing(path -> path.getFileName().toString()))
                    .toList();

            for (Path file : files) {
                String content = Files.readString(file);
                for (String chunkText : splitIntoChunks(content)) {
                    KnowledgeChunk chunk = new KnowledgeChunk(file.getFileName().toString(), chunkText);
                    Embedding embedding = embeddingModel.embed(chunkText).content();
                    store.add(embedding, chunk);
                }
            }

            return new KnowledgeBase(embeddingModel, store);
        } catch (IOException exception) {
            throw new IllegalStateException("Failed to load local knowledge base", exception);
        }
    }

    List<RetrievedChunk> retrieve(String query, int maxResults) {
        Embedding queryEmbedding = embeddingModel.embed(query).content();
        EmbeddingSearchRequest searchRequest = EmbeddingSearchRequest.builder()
                .queryEmbedding(queryEmbedding)
                .maxResults(maxResults)
                .build();
        EmbeddingSearchResult<KnowledgeChunk> searchResult = store.search(searchRequest);
        return searchResult.matches().stream()
                .map(match -> new RetrievedChunk(match.embedded().source(), match.score(), match.embedded().text()))
                .toList();
    }

    private static List<String> splitIntoChunks(String content) {
        String[] paragraphs = content.split("\\R\\R+");
        List<String> chunks = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        for (String paragraph : paragraphs) {
            String trimmed = paragraph.trim();
            if (trimmed.isBlank()) {
                continue;
            }
            if (current.length() + trimmed.length() > 550 && current.length() > 0) {
                chunks.add(current.toString().trim());
                current = new StringBuilder();
            }
            current.append(trimmed).append(System.lineSeparator()).append(System.lineSeparator());
        }
        if (current.length() > 0) {
            chunks.add(current.toString().trim());
        }
        return chunks;
    }

    record KnowledgeChunk(String source, String text) {
        @Override
        public String toString() {
            return source + ":" + text.substring(0, Math.min(text.length(), 80)).toLowerCase(Locale.ROOT);
        }
    }

    record RetrievedChunk(String source, double score, String text) {
    }
}
