<script lang="ts">
	import { eventNames, eventSolves, type CompetitionResults, type WCAEvent } from '$lib/types';
	import { bestTime, calculateWCAAverage, compareTimes, renderTime } from '$lib/utils';

	let { competitionResults }: { competitionResults: CompetitionResults } = $props();

	let sortedResults = $derived(
		competitionResults.results.map(({ event, rounds }) => ({
			event,
			rounds: rounds.map(({ round, results }) => ({
				round,
				results: results.slice().sort((a, b) => compareTimes(event, a.times, b.times))
			}))
		}))
	);

	let innerWidth = $state<number>(0);
	let selectedPerson = $state<{ name: string; times: number[] } | null>(null);
	let selectedEvent = $state<WCAEvent>('333');
	let showModal = $state<boolean>(false);
</script>

<svelte:window bind:innerWidth />
<div class="mx-4 my-2">
	<h1 class="mb-4 text-2xl font-bold">Results for {competitionResults.competition.name}</h1>
	<div class="w-full space-y-6">
		{#each sortedResults as { event, rounds }}
			<div class="rounded-lg bg-white p-1 shadow">
				{#each rounds as { round, results }}
					<div>
						<h2 class="mb-2 text-xl font-semibold ms-2">
							{eventNames[event]} - Round {round}
						</h2>
						<div class="overflow-x-auto rounded-md">
							<table class="w-full">
								<thead class="bg-gray-200">
									<tr>
										<th class="px-4 py-2 text-center">#</th>
										<th class="px-4 py-2 text-center">Name</th>
										{#each Array.from({ length: eventSolves[event]! }) as _, idx}
											<th class="hidden px-4 py-2 text-center md:table-cell">{idx + 1}</th>
										{/each}
										<th class="px-4 py-2 text-center">Average</th>
										<th class="px-4 py-2 text-center">Best</th>
									</tr>
								</thead>
								<tbody class="bg-gray-100">
									{#each results as roundPerson, index}
										<tr>
											{#if index != 0}
												<td colspan="100">
													<hr />
												</td>
											{/if}
										</tr>
										<tr
											class="hover:bg-gray-50"
											onclick={() => {
												if (innerWidth > 768) return;
												selectedPerson = roundPerson;
												selectedEvent = event;
												showModal = true;
											}}
										>
											<td class="px-4 py-2 text-center">{index + 1}</td>
											<td class="px-4 py-2 text-center">{roundPerson.name}</td>
											{#each roundPerson.times as time}
												<td class="hidden px-4 py-2 text-center md:table-cell">
													{renderTime(time)}
												</td>
											{/each}
											<td class="px-4 py-2 text-center">
												{renderTime(calculateWCAAverage(event, roundPerson.times))}
											</td>
											<td class="px-4 py-2 text-center">
												{renderTime(bestTime(roundPerson.times))}
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/each}
			</div>
		{/each}
	</div>
</div>

{#if showModal && selectedPerson}
	<div
		class="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50 p-4"
		onclick={() => (showModal = false)}
		onkeydown={(e) => e.key === 'Enter' && (showModal = false)}
		aria-label="Close modal"
		role="button"
		tabindex="0"
	>
		<div class="w-full max-w-lg rounded-lg bg-white p-6" role="dialog" aria-modal="true">
			<h3 class="mb-4 text-xl font-semibold">{selectedPerson.name}</h3>
			<div class="grid grid-cols-2 gap-4">
				<div class="bold">Attempts</div>
				<div>{selectedPerson.times.map(renderTime).join(', ')}</div>
				<div>Average</div>
				<div>{calculateWCAAverage(selectedEvent as WCAEvent, selectedPerson.times)}</div>
				<div>Best</div>
				<div>{bestTime(selectedPerson.times)}</div>
			</div>
			<button
				class="mt-4 rounded bg-gray-200 px-4 py-2 hover:bg-gray-300"
				onclick={() => (showModal = false)}
			>
				Close
			</button>
		</div>
	</div>
{/if}
