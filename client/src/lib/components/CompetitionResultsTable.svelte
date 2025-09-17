<script lang="ts">
import { eventNames, eventSolves, type ResultsTableCompetition, type WCAEvent } from '$lib/types';
import { getMeanType, renderTime, sortEvents } from '$lib/utils';
import EventPicker from './EventPicker.svelte';

interface ResultsTableProp {
	event: WCAEvent;
	results: ResultsTableCompetition[];
}

let {
	results,
	selectedEvent
}: {
	results: ResultsTableProp[];
	selectedEvent: WCAEvent;
} = $props();

const validEvents = $derived(results.map((result) => result.event).sort(sortEvents));

let selectedEventData = $derived(
	results.find((event) => event.event === selectedEvent)?.results ?? []
);
</script>

<div class="overflow-hidden rounded-lg bg-white shadow-sm">
	{#if results.length > 0}
		<div class="my-4 flex justify-center">
			<EventPicker bind:selectedEvent={selectedEvent} events={validEvents} />
		</div>

		<div class="border-b border-gray-200 px-6 pb-4">
			<h2 class="text-xl font-semibold text-gray-800">
				Results for {eventNames[selectedEvent]}
			</h2>
		</div>
		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-gray-200">
				<thead class="bg-gray-50">
					<tr>
						<th
							class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
						>
							Competition
						</th>
						<th
							class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
						>
							Round
						</th>
						<th
							class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
						>
							Single
						</th>
						<th
							class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
						>
							{getMeanType(selectedEvent)}
						</th>
						{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
							<th
								class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
							>
								Solve {idx + 1}
							</th>
						{/each}
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-200 bg-white">
					{#each selectedEventData as competition (competition.id)}
						{#each competition.rounds as round, roundIndex (round.round)}
							<tr class="transition-colors duration-100 ease-in-out hover:bg-gray-100">
								<td class="px-6 py-4 text-sm whitespace-nowrap text-gray-900">
									{#if roundIndex === 0}
										<a href="/competitions/{competition.id}" class="hover:text-gray-400">
											{competition.name}
										</a>
									{/if}
								</td>
								<td class="px-6 py-4 text-center text-sm whitespace-nowrap text-gray-900">
									{round.round}
								</td>
								<td
									class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap {round.singleRecord ? 'text-blue-600' : 'text-gray-900'}"
								>
									{renderTime(round.single)}
								</td>
								<td
									class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap {round.averageRecord ? 'text-blue-600' : 'text-gray-900'}"
								>
									{renderTime(round.average)}
								</td>
								{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
									<td
										class="px-6 py-4 text-center font-mono text-sm whitespace-nowrap text-gray-700"
									>
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
		<div class="rounded-lg bg-white p-8 text-center shadow-sm">
			<h3 class="text-lg font-medium text-gray-900">No results found</h3>
		</div>
	{/if}
</div>
