<script lang="ts">
import { Portal } from "bits-ui";
import { type CompetitionResults, type PersonResult, type WCAEvent, eventNames, eventSolves } from "$lib/types";
import { compareResults, getDroppedIndices, getMeanType, renderTime, sortEvents } from "$lib/utils";

const BREAKPOINT = 835;

const { competitionResults }: { competitionResults: CompetitionResults } = $props();

const sortedResults = $derived(
	competitionResults.results
		.map(({ event, rounds }) => ({
			event,
			rounds: rounds.map(({ round, results }) => ({
				results: [...results].toSorted((a, b) => compareResults(a, b)),
				round,
			})),
		}))
		.toSorted((a, b) => sortEvents(a.event, b.event)),
);

let innerWidth = $state<number>(0);
let selectedPerson = $state<PersonResult | null>(null);
let selectedEvent = $state<WCAEvent>("333");
let selectedRound = $state<number>(1);
let showModal = $state<boolean>(false);

const trimResults = $derived(innerWidth < BREAKPOINT);

$effect(() => {
	if (showModal) {
		const originalOverflow = document.body.style.overflow;
		document.body.style.overflow = "hidden";
		return () => {
			document.body.style.overflow = originalOverflow;
		};
	}
});
</script>

<svelte:window bind:innerWidth />

<div class="space-y-6">
	{#each sortedResults as { event, rounds } (event)}
		<section id="event-{event}" class="scroll-mt-24 space-y-4">
			{#each rounds as { round, results }, roundIndex (round)}
				<div class="overflow-hidden border border-gray-200 bg-white">
					<!-- Flat Institutional Header Banner -->
					<div
						class="flex items-center justify-between border-b border-gray-200 bg-uoft-blue px-4 py-2.5 text-white sm:px-5"
					>
						<div class="flex items-center gap-2.5">
							<div class="flex h-7 w-7 items-center justify-center rounded-sm bg-white/15 text-white">
								<span class="cubing-icon event-{event} text-base"></span>
							</div>
							<h2 class="text-sm font-bold tracking-tight text-white sm:text-base">
								{eventNames[event]}
							</h2>
							<span class="rounded-sm bg-white/15 px-2 py-0.5 text-xs font-semibold text-white">
								Round {round}
							</span>
						</div>
					</div>

					<!-- Results Table -->
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50">
								<tr>
									<th class="w-12 px-3 py-2.5 text-center text-xs font-semibold tracking-wider text-gray-700 uppercase">
										#
									</th>
									<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase">
										Name
									</th>
									{#each Array.from({ length: eventSolves[event]! }).keys() as idx (idx)}
										<th
											class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
											class:hidden={trimResults}
										>
											Solve {idx + 1}
										</th>
									{/each}
									<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase">
										Best
									</th>
									<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-uoft-blue uppercase">
										{getMeanType(event)}
									</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-100 bg-white">
								{#each results as roundPerson, index (roundPerson.id ?? index)}
									{@const droppedIndices = getDroppedIndices(roundPerson.times)}
									<tr
										class="transition-colors hover:bg-gray-50/80"
										class:cursor-pointer={trimResults}
										onclick={(e) => {
											if (!trimResults) {
												return;
											}
											if (e.target instanceof Element && e.target.closest("a")) {
												return;
											}
											selectedPerson = roundPerson;
											selectedEvent = event;
											selectedRound = round;
											showModal = true;
										}}
									>
										<!-- Rank (Clean typographic) -->
										<td
											class="w-12 px-3 py-2.5 text-center font-mono text-xs font-semibold whitespace-nowrap tabular-nums"
										>
											{#if index === 0}
												<span class="font-bold text-amber-600">1</span>
											{:else if index === 1}
												<span class="font-bold text-gray-700">2</span>
											{:else if index === 2}
												<span class="font-bold text-amber-800">3</span>
											{:else}
												<span class="font-medium text-gray-700">{index + 1}</span>
											{/if}
										</td>

										<!-- Competitor Name & subtle tag -->
										<td class="px-4 py-2.5 text-left text-sm whitespace-nowrap">
											<div class="flex items-center gap-2">
												<a
													href="/persons/{roundPerson.person}"
													class="font-medium text-gray-900 transition-colors hover:text-uoft-blue hover:underline"
												>
													{roundPerson.person_name}
												</a>
												{#if "student_designator" in roundPerson && roundPerson.student_designator}
													<span
														class="rounded-sm bg-gray-100 px-1.5 py-0.5 text-[10px] font-medium text-gray-600 uppercase"
													>
														{roundPerson.student_designator}
													</span>
												{/if}
											</div>
										</td>

										<!-- Solves 1 to 5 (hidden on mobile) -->
										{#each roundPerson.times as time, timeIdx (timeIdx)}
											{@const isDropped = droppedIndices.has(timeIdx)}
											{@const isDNF = time < 0}
											<td
												class="px-4 py-2.5 text-right font-mono text-sm whitespace-nowrap tabular-nums"
												class:hidden={trimResults}
											>
												{#if isDropped}
													<span class="font-normal text-gray-700">
														({renderTime(time)})
													</span>
												{:else if isDNF}
													<span class="font-semibold text-uoft-warm-red">
														{renderTime(time)}
													</span>
												{:else}
													<span class="text-gray-700">
														{renderTime(time)}
													</span>
												{/if}
											</td>
										{/each}

										<!-- Best Single -->
										<td
											class="px-4 py-2.5 text-right font-mono text-sm font-semibold whitespace-nowrap text-gray-900 tabular-nums"
										>
											{renderTime(roundPerson.single)}
										</td>

										<!-- Average / Mean -->
										<td
											class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-uoft-blue tabular-nums"
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
		</section>
	{:else}
		<div class="border border-gray-200 bg-white p-12 text-center">
			<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-sm bg-gray-100 text-uoft-blue">
				<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
					/>
				</svg>
			</div>
			<h3 class="mt-3 text-base font-bold text-gray-900">No Results Found</h3>
			<p class="mt-1 text-xs text-gray-700">Results for the selected filter or round have not been recorded yet.</p>
		</div>
	{/each}
</div>

<!-- Mobile Competitor Solve Breakdown Modal -->
{#if showModal && selectedPerson}
	{@const droppedIndices = getDroppedIndices(selectedPerson.times)}
	<Portal>
		<div
			class="fixed inset-0 z-50 flex h-full min-h-[100dvh] w-full items-center justify-center bg-black/50 p-4 backdrop-blur-xs"
			onclick={() => (showModal = false)}
			onkeydown={(e) => e.key === "Escape" && (showModal = false)}
			aria-label="Close modal"
			role="button"
			tabindex="0"
		>
			<div
				class="w-full max-w-md overflow-hidden border border-gray-300 bg-white"
				role="dialog"
				aria-modal="true"
				tabindex="0"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.key === "Escape" && (showModal = false)}
			>
				<!-- Modal Header in U of T Blue -->
				<div class="flex items-center justify-between border-b border-gray-200 bg-uoft-blue px-5 py-3 text-white">
					<div>
						<h3 class="text-base font-bold text-white">{selectedPerson.person_name}</h3>
						<p class="text-xs text-blue-200">
							{eventNames[selectedEvent]} • Round {selectedRound}
						</p>
					</div>
					<button
						type="button"
						class="p-1 text-white/80 hover:text-white"
						onclick={() => (showModal = false)}
						aria-label="Close"
					>
						<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
				</div>

				<!-- Solve Details -->
				<div class="space-y-4 p-5">
					<!-- Solves breakdown -->
					<div>
						<h4 class="mb-2 text-xs font-semibold tracking-wider text-gray-700 uppercase">Individual Solves</h4>
						<div class="grid grid-cols-5 gap-1.5">
							{#each selectedPerson.times as time, idx (idx)}
								{@const isDropped = droppedIndices.has(idx)}
								{@const isDNF = time < 0}
								<div class="border border-gray-200 bg-gray-50 p-2 text-center">
									<div class="text-[10px] font-semibold text-gray-700">S{idx + 1}</div>
									<div
										class="mt-0.5 font-mono text-xs font-bold tabular-nums"
										class:text-gray-700={isDropped}
										class:text-uoft-warm-red={isDNF}
										class:text-gray-900={!isDropped && !isDNF}
									>
										{#if isDropped}
											({renderTime(time)})
										{:else}
											{renderTime(time)}
										{/if}
									</div>
								</div>
							{/each}
						</div>
					</div>

					<!-- Summary metrics -->
					<div class="grid grid-cols-2 gap-3 border border-gray-200 bg-gray-50 p-3">
						<div>
							<div class="text-xs text-gray-600">Best Single</div>
							<div class="mt-0.5 font-mono text-lg font-bold text-gray-900 tabular-nums">
								{renderTime(selectedPerson.single)}
							</div>
						</div>
						<div>
							<div class="text-xs text-uoft-blue">{getMeanType(selectedEvent)}</div>
							<div class="mt-0.5 font-mono text-lg font-bold text-uoft-blue tabular-nums">
								{renderTime(selectedPerson.average)}
							</div>
						</div>
					</div>

					<div class="flex items-center justify-between pt-2">
						<a href="/persons/{selectedPerson.person}" class="text-xs font-medium text-uoft-blue hover:underline">
							View Competitor Profile →
						</a>
						<button
							type="button"
							class="rounded-sm bg-uoft-blue px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 focus:outline-none"
							onclick={() => (showModal = false)}
						>
							Close
						</button>
					</div>
				</div>
			</div>
		</div>
	</Portal>
{/if}
