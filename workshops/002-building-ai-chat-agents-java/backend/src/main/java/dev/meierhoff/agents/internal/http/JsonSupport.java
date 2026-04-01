package dev.meierhoff.agents.internal.http;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.databind.json.JsonMapper;
import dev.meierhoff.agents.workshop.api.ChatRequestPayload;

import java.io.IOException;
import java.io.InputStream;

final class JsonSupport {

    private final ObjectMapper mapper = JsonMapper.builder()
            .findAndAddModules()
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS)
            .disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES)
            .build();

    /**
     * Parses the JSON body of `POST /chat`.
     */
    ChatRequestPayload readChatRequest(InputStream inputStream) throws IOException {
        return mapper.readValue(inputStream, ChatRequestPayload.class);
    }

    /**
     * Serializes a response object as pretty-printed JSON for easier manual
     * inspection during the workshop.
     */
    byte[] writeBytes(Object value) throws JsonProcessingException {
        return mapper.writerWithDefaultPrettyPrinter().writeValueAsBytes(value);
    }
}
