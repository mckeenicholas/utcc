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

<div class="overflow-hidden border border-border bg-surface">
	{#if results.length > 0}
		<div class="border-b border-border bg-surface-subtle p-3 sm:p-4">
			<EventPicker bind:selectedEvent events={validEvents} />
		</div>

		<div class="border-b border-border bg-surface px-4 py-2.5 sm:px-5">
			<h2 class="text-sm font-bold tracking-tight text-main">
				Competition Solves: {eventNames[selectedEvent]}
			</h2>
		</div>

		<div class="overflow-x-auto">
			<table class="min-w-full divide-y divide-border">
				<thead class="bg-surface-subtle">
					<tr>
						<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-secondary uppercase">
							Competition
						</th>
						<th class="px-4 py-2.5 text-center text-xs font-semibold tracking-wider text-secondary uppercase">
							Round
						</th>
						<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase">
							Single
						</th>
						<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-brand uppercase">
							{getMeanType(selectedEvent)}
						</th>
						{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
							<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase">
								Solve {idx + 1}
							</th>
						{/each}
					</tr>
				</thead>
				<tbody class="divide-y divide-border bg-surface">
					{#each selectedEventData as competition (competition.id)}
						{#each competition.rounds as round, roundIndex (round.round)}
							<tr class="transition-colors hover:bg-surface-muted">
								<td class="px-4 py-2.5 text-sm whitespace-nowrap text-main">
									{#if roundIndex === 0}
										<a href="/competitions/{competition.id}" class="font-medium transition-colors hover:text-brand">
											{competition.name}
										</a>
									{/if}
								</td>
								<td class="px-4 py-2.5 text-center font-mono text-xs whitespace-nowrap text-secondary">
									{round.round}
								</td>
								<td
									class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap tabular-nums {round.singleRecord
										? 'text-secondary-cyan dark:text-secondary-cyan-80'
										: 'text-main'}"
								>
									{renderTime(round.single)}
								</td>
								<td
									class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap tabular-nums {round.averageRecord
										? 'text-secondary-cyan dark:text-secondary-cyan-80'
										: 'text-brand'}"
								>
									{renderTime(round.average)}
								</td>
								{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
									<td class="px-4 py-2.5 text-right font-mono text-sm whitespace-nowrap text-secondary tabular-nums">
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
		<div class="border border-border bg-surface p-8 text-center">
			<h3 class="text-sm font-medium text-main">No results found for this event.</h3>
		</div>
	{/if}
</div>
