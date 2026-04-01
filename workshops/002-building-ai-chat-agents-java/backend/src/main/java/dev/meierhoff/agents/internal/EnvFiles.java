package dev.meierhoff.agents.internal;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

final class EnvFiles {

    private EnvFiles() {
    }

    static Map<String, String> load(Path workshopRoot) {
        Map<String, String> values = new LinkedHashMap<>();
        mergeIfPresent(values, workshopRoot.resolve(".env"));
        mergeIfPresent(values, workshopRoot.resolve("backend").resolve(".env"));
        return values;
    }

    private static void mergeIfPresent(Map<String, String> values, Path file) {
        if (!Files.exists(file)) {
            return;
        }

        try {
            List<String> lines = Files.readAllLines(file);
            for (String rawLine : lines) {
                String line = rawLine.trim();
                if (line.isBlank() || line.startsWith("#")) {
                    continue;
                }
                int separatorIndex = line.indexOf('=');
                if (separatorIndex < 1) {
                    continue;
                }

                String key = line.substring(0, separatorIndex).trim();
                String value = line.substring(separatorIndex + 1).trim();
                values.put(key, stripQuotes(value));
            }
        } catch (IOException exception) {
            throw new IllegalStateException("Failed to read env file: " + file, exception);
        }
    }

    private static String stripQuotes(String value) {
        if (value.length() >= 2) {
            boolean doubleQuoted = value.startsWith("\"") && value.endsWith("\"");
            boolean singleQuoted = value.startsWith("'") && value.endsWith("'");
            if (doubleQuoted || singleQuoted) {
                return value.substring(1, value.length() - 1);
            }
        }
        return value;
    }
}
