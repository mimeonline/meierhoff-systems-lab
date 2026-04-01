package dev.meierhoff.agents.internal.config;

import java.nio.file.Files;
import java.nio.file.Path;

final class ProjectPaths {

    private ProjectPaths() {
    }

    /**
     * Walks upward from the current directory until the workshop root is found.
     *
     * <p>This makes it possible to start the backend either from the workshop
     * root or from the `backend/` directory.
     */
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
