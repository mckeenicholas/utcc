<script lang="ts">
import {
	eventListIdx,
	eventNames,
	eventSolves,
	type CompetitionResults,
	type PersonResult,
	type WCAEvent
} from '$lib/types';
import { compareResults, getMeanType, renderTime } from '$lib/utils';

const BREAKPOINT = 835;

let { competitionResults }: { competitionResults: CompetitionResults } = $props();

let sortedResults = $derived(
	competitionResults.results
		.map(({ event, rounds }) => ({
			event,
			rounds: rounds.map(({ round, results }) => ({
				round,
				results: results.slice().sort((a, b) => compareResults(a, b))
			}))
		}))
		.sort((a, b) => eventListIdx[a.event] - eventListIdx[b.event])
);

let innerWidth = $state<number>(0);
let selectedPerson = $state<PersonResult | null>(null);
let selectedEvent = $state<WCAEvent>('333');
let showModal = $state<boolean>(false);

let trimResults = $derived(innerWidth < BREAKPOINT);
</script>

<svelte:window bind:innerWidth={innerWidth} />
<div class="space-y-6">
	<div class="space-y-6">
		{#if competitionResults.results.length == 0}
			<div class="px-6 py-8 text-center">
				<div class="text-gray-500">
					<svg
						class="mx-auto h-12 w-12 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
						/>
					</svg>
					<h3 class="mt-2 text-sm font-medium text-gray-900">No Results Entered</h3>
					<p class="mt-1 text-sm text-gray-500">
						Results for this round have not been entered yet.
					</p>
				</div>
			</div>
		{:else}
			{#each sortedResults as { event, rounds } (event)}
				<div class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
					{#each rounds as { round, results }, roundIndex (round)}
						<div class="border-b border-gray-200 last:border-b-0">
							<div
								class=" border-b border-gray-200 px-4 py-2"
								class:rounded-t-lg={roundIndex === 0}
							>
								<h2 class="text-lg font-semibold text-gray-800">
									{eventNames[event]} - Round {round}
								</h2>
							</div>
							<div class="overflow-x-auto">
								<table class="min-w-full divide-y divide-gray-200">
									<thead class="">
										<tr>
											<th
												class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500"
												>#</th
											>
											<th
												class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500"
												>Name</th
											>
											{#each Array.from({ length: eventSolves[event]! }).keys() as idx (idx)}
												<th
													class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
													class:hidden={trimResults}
												>
													Solve {idx + 1}
												</th>
											{/each}
											<th
												class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
												>Best</th
											>
											<th
												class="px-6 py-3 text-right text-xs font-medium uppercase tracking-wider text-gray-500"
												>{getMeanType(event)}</th
											>
										</tr>
									</thead>
									<tbody class="divide-y divide-gray-200 bg-white">
										{#each results as roundPerson, index (index)}
											{#if index > 0}
												<tr><td colspan="100" class="h-0 border-t border-gray-100 p-0"></td></tr>
											{/if}
											<tr
												class="hover: transition-colors duration-150 ease-in-out hover:bg-gray-100"
												class:cursor-pointer={trimResults}
												onclick={() => {
													if (!trimResults) return;
													selectedPerson = roundPerson;
													selectedEvent = event;
													showModal = true;
												}}
											>
												<td
													class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900"
												>
													{index + 1}
												</td>
												<td
													class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900"
												>
													{roundPerson.person_name}
												</td>
												{#each roundPerson.times as time, timeIdx (timeIdx)}
													<td
														class="whitespace-nowrap px-6 py-4 text-right font-mono text-sm text-gray-700"
														class:hidden={trimResults}
													>
														{renderTime(time)}
													</td>
												{/each}
												<td
													class="whitespace-nowrap px-6 py-4 text-right font-mono text-sm font-medium text-gray-900"
												>
													{renderTime(roundPerson.single)}
												</td>
												<td
													class="whitespace-nowrap px-6 py-4 text-right font-mono text-sm font-medium text-gray-900"
												>
													{renderTime(roundPerson.average)}
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
		{/if}
	</div>
</div>

{#if showModal && selectedPerson}
	<div
		class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4"
		onclick={() => (showModal = false)}
		onkeydown={(e) => e.key === 'Escape' && (showModal = false)}
		aria-label="Close modal"
		role="button"
		tabindex="0"
	>
		<div
			class="w-full max-w-lg rounded-lg bg-white shadow-xl"
			role="dialog"
			aria-modal="true"
			tabindex="0"
			onclick={(e) => e.stopPropagation()}
			onkeydown={(e) => e.key === 'Escape' && (showModal = false)}
		>
			<div class="border-b border-gray-200 px-6 py-4">
				<h3 class="text-lg font-semibold text-gray-900">{selectedPerson.person_name}</h3>
				<p class="mt-1 text-sm text-gray-600">{eventNames[selectedEvent]} - Details</p>
			</div>
			<div class="px-6 py-4">
				<div class="space-y-4">
					<div class="grid grid-cols-2 gap-4">
						<div class="text-sm font-medium text-gray-700">Attempts:</div>
						<div class="font-mono text-sm text-gray-900">
							{selectedPerson.times
								.filter((time) => time != 0)
								.map(renderTime)
								.join(', ')}
						</div>
						<div class="text-sm font-medium text-gray-700">Best Single:</div>
						<div class="font-mono text-sm font-medium text-gray-900">
							{renderTime(selectedPerson.single)}
						</div>
						<div class="text-sm font-medium text-gray-700">{getMeanType(selectedEvent)}:</div>
						<div class="font-mono text-sm font-medium text-gray-900">
							{renderTime(selectedPerson.average)}
						</div>
					</div>
				</div>
			</div>
			<div class="flex justify-end border-t border-gray-200 px-6 py-4">
				<button
					class="inline-flex items-center rounded-md bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
					onclick={() => (showModal = false)}
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
