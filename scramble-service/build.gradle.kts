plugins {
    kotlin("jvm") version "1.6.21"
    kotlin("plugin.spring") version "1.6.21"  // ADD THIS LINE
    id("org.springframework.boot") version "2.5.4"
    id("io.spring.dependency-management") version "1.0.11.RELEASE"
}

group = "org.utcc"
version = "0.0.1-SNAPSHOT"
java.sourceCompatibility = JavaVersion.VERSION_17

repositories {
    mavenCentral()
}

dependencies {
    implementation("org.springframework.boot:spring-boot-starter-web")
    implementation("org.worldcubeassociation.tnoodle:lib-scrambles:0.19.2")
    implementation("com.fasterxml.jackson.module:jackson-module-kotlin")  // Also recommended for Kotlin
    implementation("org.jetbrains.kotlin:kotlin-reflect")  // Required for Spring
    implementation("org.jetbrains.kotlin:kotlin-stdlib-jdk8")  // Required for Kotlin
    testImplementation("org.springframework.boot:spring-boot-starter-test")
}

tasks.withType<org.jetbrains.kotlin.gradle.tasks.KotlinCompile> {
    kotlinOptions {
        jvmTarget = "11"
        freeCompilerArgs = listOf("-Xjsr305=strict")  // Recommended for Spring
    }
}

tasks.withType<Test> {
    useJUnitPlatform()
}

springBoot {
    mainClass.set("org.utcc.ApplicationKt")
}