package dev.meierhoff.agents.internal.debug;

import dev.meierhoff.agents.workshop.phases.WorkshopPhase;

/**
 * Carries phase and session information through the current call stack so debug
 * hooks can enrich the right session without polluting the visible workshop API.
 */
public final class InvocationScope {

    private static final ThreadLocal<InvocationContext> CURRENT = new ThreadLocal<>();

    private InvocationScope() {
    }

    public static InvocationContext current() {
        return CURRENT.get();
    }

    public static <T> T with(WorkshopPhase phase, String sessionId, ThrowingSupplier<T> supplier) {
        CURRENT.set(new InvocationContext(phase, sessionId));
        try {
            return supplier.get();
        } catch (Exception exception) {
            throw new RuntimeException(exception);
        } finally {
            CURRENT.remove();
        }
    }

    @FunctionalInterface
    public interface ThrowingSupplier<T> {
        T get() throws Exception;
    }

    public record InvocationContext(WorkshopPhase phase, String sessionId) {
    }
}
