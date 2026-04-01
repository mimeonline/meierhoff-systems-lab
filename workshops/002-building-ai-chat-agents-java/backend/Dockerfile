FROM maven:3.9.9-eclipse-temurin-21 AS build
WORKDIR /app

COPY pom.xml .
COPY src ./src

RUN mvn -Dmaven.repo.local=/tmp/.m2 -q package

FROM eclipse-temurin:21-jre
WORKDIR /app

COPY --from=build /app/target/langchain4j-java-workshop-0.1.0-SNAPSHOT.jar /app/workshop.jar

EXPOSE 8080

CMD ["java", "-jar", "/app/workshop.jar"]
