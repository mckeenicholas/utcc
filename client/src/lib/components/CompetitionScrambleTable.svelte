<script lang="ts">
import { type EventResult, eventListIdx, type ScrambleKey } from "$lib/types";
import { scrambleOrder } from "$lib/utils";
import CompetitionScrambleItem from "./CompetitionScrambleItem.svelte";

const { results }: { results: EventResult[] } = $props();

const scrambles = $derived(
	results
		.map((result) => ({
			event: result.event,
			rounds: result.rounds
				.map((round) => ({
					roundNum: round.round,
					sets: round.scramble_sets
						.map((set) => {
							const setScrambles = set.scrambles
								.map((scramble) => ({
									num: scramble.scramble_num.toString(),
									scramble: scramble.scramble,
								}))
								.filter((s) => s.scramble && s.scramble.length > 0)
								.toSorted(
									(a, b) =>
										(scrambleOrder[a.num as ScrambleKey]?.idx ?? 0) - (scrambleOrder[b.num as ScrambleKey]?.idx ?? 0),
								);

							return {
								num: set.scramble_set,
								scrambles: setScrambles,
							};
						})
						.filter((set) => set.scrambles.length > 0)
						.toSorted((a, b) => a.num - b.num),
				}))
				.filter((round) => round.sets.length > 0)
				.toSorted((a, b) => a.roundNum - b.roundNum),
		}))
		.filter((event) => event.rounds.length > 0)
		.toSorted((a, b) => eventListIdx[a.event] - eventListIdx[b.event]),
);
</script>

<div class="space-y-4">
	{#if scrambles.length}
		<div class="text-xs font-semibold tracking-wider text-gray-700 uppercase">Official Scrambles</div>
	{/if}

	{#each scrambles as eventScramble (eventScramble.event)}
		<CompetitionScrambleItem {eventScramble} />
	{/each}
</div>
