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
				<div class="overflow-hidden border border-border bg-surface">
					<!-- Flat Institutional Header Banner -->
					<div
						class="flex items-center justify-between border-b border-border bg-uoft-blue px-4 py-2.5 text-white sm:px-5"
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
						<table class="min-w-full divide-y divide-border">
							<thead class="bg-surface-subtle">
								<tr>
									<th
										class="w-12 px-3 py-2.5 text-center text-xs font-semibold tracking-wider text-secondary uppercase"
									>
										#
									</th>
									<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-secondary uppercase">
										Name
									</th>
									{#each Array.from({ length: eventSolves[event]! }).keys() as idx (idx)}
										<th
											class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
											class:hidden={trimResults}
										>
											Solve {idx + 1}
										</th>
									{/each}
									<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase">
										Best
									</th>
									<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-brand uppercase">
										{getMeanType(event)}
									</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-border bg-surface">
								{#each results as roundPerson, index (roundPerson.id ?? index)}
									{@const droppedIndices = getDroppedIndices(roundPerson.times)}
									<tr
										class="transition-colors hover:bg-surface-muted"
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
												<span class="font-bold text-amber-600 dark:text-amber-400">1</span>
											{:else if index === 1}
												<span class="font-bold text-secondary">2</span>
											{:else if index === 2}
												<span class="font-bold text-amber-800 dark:text-amber-500">3</span>
											{:else}
												<span class="font-medium text-secondary">{index + 1}</span>
											{/if}
										</td>

										<!-- Competitor Name & subtle tag -->
										<td class="px-4 py-2.5 text-left text-sm whitespace-nowrap">
											<div class="flex items-center gap-2">
												<a
													href="/persons/{roundPerson.person}"
													class="font-medium text-main transition-colors hover:text-brand hover:underline"
												>
													{roundPerson.person_name}
												</a>
												{#if "student_designator" in roundPerson && roundPerson.student_designator}
													<span
														class="rounded-sm bg-surface-muted px-1.5 py-0.5 text-[10px] font-medium text-secondary uppercase"
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
													<span class="font-normal text-muted">
														({renderTime(time)})
													</span>
												{:else if isDNF}
													<span class="font-semibold text-uoft-warm-red dark:text-red-400">
														{renderTime(time)}
													</span>
												{:else}
													<span class="text-secondary">
														{renderTime(time)}
													</span>
												{/if}
											</td>
										{/each}

										<!-- Best Single -->
										<td
											class="px-4 py-2.5 text-right font-mono text-sm font-semibold whitespace-nowrap text-main tabular-nums"
										>
											{renderTime(roundPerson.single)}
										</td>

										<!-- Average / Mean -->
										<td
											class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-brand tabular-nums"
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
		<div class="border border-border bg-surface p-12 text-center">
			<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-sm bg-surface-muted text-brand">
				<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
					/>
				</svg>
			</div>
			<h3 class="mt-3 text-base font-bold text-main">No Results Found</h3>
			<p class="mt-1 text-xs text-secondary">Results for the selected filter or round have not been recorded yet.</p>
		</div>
	{/each}
</div>

<!-- Mobile Competitor Solve Breakdown Modal -->
{#if showModal && selectedPerson}
	{@const droppedIndices = getDroppedIndices(selectedPerson.times)}
	<Portal>
		<div
			class="fixed inset-0 z-50 flex h-full min-h-dvh w-full items-center justify-center bg-black/50 p-4 backdrop-blur-xs"
			onclick={() => (showModal = false)}
			onkeydown={(e) => e.key === "Escape" && (showModal = false)}
			aria-label="Close modal"
			role="button"
			tabindex="0"
		>
			<div
				class="w-full max-w-md overflow-hidden border border-border-strong bg-surface"
				role="dialog"
				aria-modal="true"
				tabindex="0"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.key === "Escape" && (showModal = false)}
			>
				<!-- Modal Header in U of T Blue -->
				<div class="flex items-center justify-between border-b border-border bg-uoft-blue px-5 py-3 text-white">
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
						<h4 class="mb-2 text-xs font-semibold tracking-wider text-secondary uppercase">Solves</h4>
						<div class="grid grid-cols-5 gap-1.5">
							{#each selectedPerson.times as time, idx (idx)}
								{@const isDropped = droppedIndices.has(idx)}
								{@const isDNF = time < 0}
								<div class="border border-border bg-surface-subtle p-2 text-center">
									<div class="text-[10px] font-semibold text-secondary">S{idx + 1}</div>
									<div
										class="mt-0.5 font-mono text-xs font-bold tabular-nums"
										class:text-muted={isDropped}
										class:text-uoft-warm-red={isDNF}
										class:dark:text-red-400={isDNF}
										class:text-main={!isDropped && !isDNF}
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
					<div class="grid grid-cols-2 gap-3 border border-border bg-surface-subtle p-3">
						<div>
							<div class="text-xs text-secondary">Best Single</div>
							<div class="mt-0.5 font-mono text-lg font-bold text-main tabular-nums">
								{renderTime(selectedPerson.single)}
							</div>
						</div>
						<div>
							<div class="text-xs text-brand">{getMeanType(selectedEvent)}</div>
							<div class="mt-0.5 font-mono text-lg font-bold text-brand tabular-nums">
								{renderTime(selectedPerson.average)}
							</div>
						</div>
					</div>

					<div class="flex items-center justify-between pt-2">
						<a href="/persons/{selectedPerson.person}" class="text-xs font-medium text-brand hover:underline">
							View Competitor Profile →
						</a>
						<button
							type="button"
							class="rounded-sm bg-uoft-blue px-3 py-1.5 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 focus:outline-none dark:border dark:border-blue-500/30"
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
