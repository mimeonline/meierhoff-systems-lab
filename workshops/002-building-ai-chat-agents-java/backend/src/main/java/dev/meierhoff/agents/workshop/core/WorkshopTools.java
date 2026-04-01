package dev.meierhoff.agents.workshop.core;

import dev.langchain4j.agent.tool.P;
import dev.langchain4j.agent.tool.Tool;

import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;

/**
 * This class intentionally stays in the visible workshop package because tool
 * methods are one of the core concepts participants should understand.
 */
final class WorkshopTools {

    @Tool("Returns the current time in Europe/Berlin as a workshop-friendly string.")
    String currentTime() {
        return ZonedDateTime.now().format(DateTimeFormatter.ISO_OFFSET_DATE_TIME);
    }

    @Tool("Calculates a result from two numbers using add, subtract, multiply, or divide.")
    double calculator(
            @P("The left-hand number") double left,
            @P("The right-hand number") double right,
            @P("The operation: add, subtract, multiply, or divide") String operation
    ) {
        return switch (operation) {
            case "add" -> left + right;
            case "subtract" -> left - right;
            case "multiply" -> left * right;
            case "divide" -> right == 0 ? Double.NaN : left / right;
            default -> throw new IllegalArgumentException("Unsupported operation: " + operation);
        };
    }
}
