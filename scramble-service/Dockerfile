FROM gradle:8.7-jdk AS builder

COPY . /home/gradle/project
WORKDIR /home/gradle/project

RUN gradle bootJar --no-daemon

FROM eclipse-temurin:17

COPY --from=builder /home/gradle/project/build/libs/*.jar app.jar

ENTRYPOINT ["java", "-jar", "/app.jar"]
