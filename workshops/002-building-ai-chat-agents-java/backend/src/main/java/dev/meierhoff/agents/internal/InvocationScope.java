package dev.meierhoff.agents.internal;

import dev.meierhoff.agents.workshop.WorkshopPhase;

final class InvocationScope {

    private static final ThreadLocal<InvocationContext> CURRENT = new ThreadLocal<>();

    private InvocationScope() {
    }

    static InvocationContext current() {
        return CURRENT.get();
    }

    static <T> T with(WorkshopPhase phase, String sessionId, ThrowingSupplier<T> supplier) {
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
    interface ThrowingSupplier<T> {
        T get() throws Exception;
    }

    record InvocationContext(WorkshopPhase phase, String sessionId) {
    }
}
