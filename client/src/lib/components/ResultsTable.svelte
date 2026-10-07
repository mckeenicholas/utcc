<script lang="ts">
import {
	eventNames,
	eventSolves,
	type CompetitionResults,
	type PersonResult,
	type Result,
	type WCAEvent,
} from "$lib/types";
import { compareResults, getMeanType, isSinglePrimaryEvent, renderTime, sortEvents } from "$lib/utils";
import CubeIcon from "./CubeIcon.svelte";

interface Props {
	competitionResults: CompetitionResults | null;
	onEdit: (result: Result) => void;
	onDelete: (resultId: number) => void;
}

const { competitionResults, onEdit, onDelete }: Props = $props();

const resultsObj = $derived.by(() => {
	if (!competitionResults) {
		return null;
	}

	return {
		...competitionResults,
		results: competitionResults.results
			.map((eventResult) => ({
				...eventResult,
				rounds: eventResult.rounds
					.map((round) => ({
						...round,
						results: [...round.results].toSorted((a, b) => compareResults(a, b, eventResult.event)),
					}))
					.toSorted((a, b) => a.round - b.round),
			}))
			.toSorted((a, b) => sortEvents(a.event, b.event)),
	};
});

const getAttemptCount = (event: WCAEvent): number => eventSolves[event] ?? 5;

const convertToResult = (
	personResult: PersonResult,
	event: WCAEvent,
	round: number,
	competitionId: number,
): Result => ({
	id: personResult.id,
	person: personResult.person,
	person_name: personResult.person_name,
	single: personResult.single,
	average: personResult.average,
	competition: competitionId,
	event,
	round,
	time1: personResult.times[0] || 0,
	time2: personResult.times[1] || 0,
	time3: personResult.times[2] || 0,
	time4: personResult.times[3] || 0,
	time5: personResult.times[4] || 0,
});
</script>

<div class="border border-border bg-surface p-5 sm:p-6">
	<h2 class="mb-5 text-base font-bold text-main">Entered Results</h2>

	{#each resultsObj?.results ?? [] as eventResult (eventResult.event)}
		{@const isSinglePrimary = isSinglePrimaryEvent(eventResult.event)}
		{@const eventAttempts = getAttemptCount(eventResult.event)}
		<div class="mb-6 last:mb-0">
			<div class="mb-3 flex items-center gap-2 border-b border-border pb-2">
				<CubeIcon event={eventResult.event} class="text-base text-brand" />
				<h3 class="text-sm font-bold text-main">{eventNames[eventResult.event]}</h3>
			</div>

			{#each eventResult.rounds as round (round.round)}
				{#if round.results.length > 0}
					<div class="mb-5">
						<h4 class="mb-2 text-xs font-semibold tracking-wider text-secondary uppercase">
							Round {round.round}
						</h4>
						<div class="overflow-x-auto border border-border">
							<table class="w-full table-fixed border-collapse">
								<colgroup>
									<col class="w-36" />
									<col class="w-20" /> <col class="w-20" /> <col class="w-20" />
									{#if eventAttempts == 5}
										<col class="w-20" />
										<col class="w-20" />
									{/if}
									<col class="w-24" />
									<col class="w-24" />
									<col class="w-28" />
								</colgroup>
								<thead class="bg-surface-subtle">
									<tr class="border-b border-border">
										<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-secondary uppercase"
											>Name</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
											>T1</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
											>T2</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
											>T3</th
										>
										{#if eventAttempts == 5}
											<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
												>T4</th
											>
											<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
												>T5</th
											>
										{/if}
										<th
											class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider uppercase"
											class:text-brand={isSinglePrimary}
											class:text-secondary={!isSinglePrimary}
										>
											Single
										</th>
										<th
											class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider uppercase"
											class:text-brand={!isSinglePrimary}
											class:text-secondary={isSinglePrimary}
										>
											{getMeanType(eventResult.event)}
										</th>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
											>Actions</th
										>
									</tr>
								</thead>
								<tbody class="divide-y divide-border bg-surface">
									{#each round.results as personResult, idx (idx)}
										{@const result = convertToResult(
											personResult,
											eventResult.event,
											round.round,
											resultsObj!.competition.id,
										)}
										<tr class="transition-colors hover:bg-surface-muted">
											<td class="truncate px-4 py-2 text-sm font-medium text-main">{personResult.person_name}</td>
											<td class="px-4 py-2 text-right font-mono text-sm text-secondary tabular-nums"
												>{renderTime(personResult.times[0] || 0)}</td
											>
											<td class="px-4 py-2 text-right font-mono text-sm text-secondary tabular-nums"
												>{renderTime(personResult.times[1] || 0)}</td
											>
											<td class="px-4 py-2 text-right font-mono text-sm text-secondary tabular-nums"
												>{renderTime(personResult.times[2] || 0)}</td
											>
											{#if eventAttempts == 5}
												<td class="px-4 py-2 text-right font-mono text-sm text-secondary tabular-nums"
													>{renderTime(personResult.times[3] || 0)}</td
												>
												<td class="px-4 py-2 text-right font-mono text-sm text-secondary tabular-nums"
													>{renderTime(personResult.times[4] || 0)}</td
												>
											{/if}
											<td
												class="px-4 py-2 text-right font-mono text-sm tabular-nums {isSinglePrimary
													? 'bg-uoft-blue/4 font-bold text-brand dark:bg-blue-500/10'
													: 'font-semibold text-main'}"
											>
												{renderTime(personResult.single)}
											</td>
											<td
												class="px-4 py-2 text-right font-mono text-sm tabular-nums {!isSinglePrimary
													? 'bg-uoft-blue/4 font-bold text-brand dark:bg-blue-500/10'
													: 'font-semibold text-main'}"
											>
												{renderTime(personResult.average)}
											</td>
											<td class="px-4 py-2 text-right">
												<div class="inline-flex items-center justify-end gap-1.5">
													<button
														type="button"
														onclick={() => onEdit(result)}
														class="cursor-pointer rounded-sm border border-border bg-surface px-2 py-0.5 text-xs font-medium text-secondary transition-colors hover:border-brand hover:bg-surface-muted"
													>
														Edit
													</button>
													<button
														type="button"
														onclick={() => onDelete(personResult.id)}
														class="cursor-pointer rounded-sm border border-red-200 bg-surface px-2 py-0.5 text-xs font-medium text-uoft-warm-red transition-colors hover:bg-red-50 dark:border-red-900/60 dark:text-red-400 dark:hover:bg-red-950/40"
													>
														Delete
													</button>
												</div>
											</td>
										</tr>
									{/each}
								</tbody>
							</table>
						</div>
					</div>
				{/if}
			{/each}
		</div>
	{:else}
		<p class="py-8 text-center text-xs text-secondary">No results submitted yet.</p>
	{/each}
</div>
