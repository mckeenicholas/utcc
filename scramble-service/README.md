# UTCC Scramble Service
This acts as a simple standalone microservice for generating WCA-compliant scrambles. It uses `org.worldcubeassociation.tnoodle/lib-scrambles`, which is the same program used to generate scrambles for WCA competitions.

### Info
This service is written in Kotlin using Spring and built with Gradle. It is designed to be deployed in a single Docker container and called from a backend service needing to generate scrambles.

Due to the computationally intensive nature of generating some scramble sequences, it is recommended that you don't expose this endpoint directly. You should also implement some authorization to prevent vulnerability to denial-of-service (DoS) attacks.