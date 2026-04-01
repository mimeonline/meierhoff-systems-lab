package dev.meierhoff.agents.internal.config;

import java.nio.file.Files;
import java.nio.file.Path;

final class ProjectPaths {

    private ProjectPaths() {
    }

    static Path detectWorkshopRoot() {
        Path current = Path.of("").toAbsolutePath();
        while (current != null) {
            if (Files.isDirectory(current.resolve("knowledge"))
                    && Files.isDirectory(current.resolve("frontend"))
                    && Files.isDirectory(current.resolve("backend"))) {
                return current;
            }
            current = current.getParent();
        }
        throw new IllegalStateException("Could not locate workshop root from current directory.");
    }
}
