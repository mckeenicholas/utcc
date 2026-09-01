<script lang="ts">
import { type ResultsTableCompetition, type WCAEvent, eventNames, eventSolves } from "$lib/types";
import { getMeanType, renderTime, sortEvents } from "$lib/utils";
import EventPicker from "./EventPicker.svelte";

interface ResultsTableProp {
	event: WCAEvent;
	results: ResultsTableCompetition[];
}

let {
	results,
	selectedEvent = $bindable("333"),
}: {
	results: ResultsTableProp[];
	selectedEvent?: WCAEvent;
} = $props();

const validEvents = $derived(results.map((result) => result.event).toSorted(sortEvents));

$effect(() => {
	if (validEvents.length > 0 && (!selectedEvent || !validEvents.includes(selectedEvent))) {
		selectedEvent = validEvents.includes("333") ? "333" : validEvents[0];
	}
});

const selectedEventData = $derived(results.find((event) => event.event === selectedEvent)?.results ?? []);
</script>

<div class="overflow-hidden border border-gray-200 bg-white">
	{#if results.length > 0}
		<div class="border-b border-gray-200 bg-gray-50/50 p-3 sm:p-4">
			<EventPicker bind:selectedEvent events={validEvents} />
		</div>

		<div class="border-b border-gray-200 bg-white px-4 py-2.5 sm:px-5">
			<h2 class="text-sm font-bold tracking-tight text-gray-900">
				Competition Solves: {eventNames[selectedEvent]}
			</h2>
		</div>

		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase">
							Competition
						</th>
						<th class="px-4 py-2.5 text-center text-xs font-semibold tracking-wider text-gray-700 uppercase">
							Round
						</th>
						<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase">
							Single
						</th>
						<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-uoft-blue uppercase">
							{getMeanType(selectedEvent)}
						</th>
						{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
							<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase">
								Solve {idx + 1}
							</th>
						{/each}
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-100 bg-white">
					{#each selectedEventData as competition (competition.id)}
						{#each competition.rounds as round, roundIndex (round.round)}
							<tr class="transition-colors hover:bg-gray-50/80">
								<td class="px-4 py-2.5 text-sm whitespace-nowrap text-gray-900">
									{#if roundIndex === 0}
										<a href="/competitions/{competition.id}" class="font-medium transition-colors hover:text-uoft-blue">
											{competition.name}
										</a>
									{/if}
								</td>
								<td class="px-4 py-2.5 text-center font-mono text-xs whitespace-nowrap text-gray-600">
									{round.round}
								</td>
								<td
									class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap tabular-nums {round.singleRecord
										? 'text-secondary-cyan'
										: 'text-gray-900'}"
								>
									{renderTime(round.single)}
								</td>
								<td
									class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap tabular-nums {round.averageRecord
										? 'text-secondary-cyan'
										: 'text-uoft-blue'}"
								>
									{renderTime(round.average)}
								</td>
								{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
									<td class="px-4 py-2.5 text-right font-mono text-sm whitespace-nowrap text-gray-600 tabular-nums">
										{renderTime(round.times[idx])}
									</td>
								{/each}
							</tr>
						{/each}
					{/each}
				</tbody>
			</table>
		</div>
	{:else}
		<div class="border border-gray-200 bg-white p-8 text-center">
			<h3 class="text-sm font-medium text-gray-900">No results found for this event.</h3>
		</div>
	{/if}
</div>
