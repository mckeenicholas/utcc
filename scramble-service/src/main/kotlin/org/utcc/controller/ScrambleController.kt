package org.utcc.controller

import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*
import org.worldcubeassociation.tnoodle.scrambles.PuzzleRegistry

data class ScrambleRequest(val puzzleType: String, val count: Int)

@RestController
@RequestMapping("/api/scrambles")
class ScrambleController {

    private val wcaEventMap = mapOf(
            "222" to PuzzleRegistry.TWO,
            "333" to PuzzleRegistry.THREE,
            "444" to PuzzleRegistry.FOUR,
            "555" to PuzzleRegistry.FIVE,
            "666" to PuzzleRegistry.SIX,
            "777" to PuzzleRegistry.SEVEN,
            "333fm" to PuzzleRegistry.THREE_FM,
            "333oh" to PuzzleRegistry.THREE,    // One-handed uses same scrambles as regular 3x3
            "333bf" to PuzzleRegistry.THREE_NI,
            "444bf" to PuzzleRegistry.FOUR_NI,
            "555bf" to PuzzleRegistry.FIVE_NI,
            "clock" to PuzzleRegistry.CLOCK,
            "skewb" to PuzzleRegistry.SKEWB,
            "sq1" to PuzzleRegistry.SQ1,
            "pyram" to PuzzleRegistry.PYRA,
            "minx" to PuzzleRegistry.MEGA,
            "333mbf" to PuzzleRegistry.THREE_NI  // Multi-blind uses same as 3x3 blindfolded
    )

    @PostMapping
    fun generateScrambles(@RequestBody request: ScrambleRequest): ResponseEntity<Any> {
        val puzzleTypeKey = request.puzzleType.lowercase()

        val puzzleRegistry = wcaEventMap[puzzleTypeKey]

        if (puzzleRegistry == null) {
            val validTypes = wcaEventMap.keys.sorted().joinToString()

            return ResponseEntity.badRequest().body(
                    mapOf(
                            "error" to "Invalid puzzleType '${request.puzzleType}'.",
                            "validPuzzleTypes" to validTypes
                    )
            )
        }

        if (request.count <= 0) {
            return ResponseEntity.badRequest().body(
                    mapOf(
                            "error" to "Count must be a positive integer.",
                            "received" to request.count
                    )
            )
        }

        return try {
            val scrambler = puzzleRegistry.scrambler
            val count = request.count.coerceIn(1, 100)
            val scrambles = scrambler.generateScrambles(count).toList()

            ResponseEntity.ok(scrambles)
        } catch (e: Exception) {
            ResponseEntity.status(500).body(mapOf("error" to "Scramble generation failed: ${e.message}"))
        }
    }
}