<script lang="ts">
import {
	eventNames,
	eventSolves,
	type CompetitionResults,
	type PersonResult,
	type Result,
	type WCAEvent,
} from "$lib/types";
import { compareResults, getMeanType, renderTime, sortEvents } from "$lib/utils";
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
				rounds: eventResult.rounds.map((round) => ({
					...round,
					results: round.results.toSorted(compareResults),
				})),
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

<div class="border border-gray-200 bg-white p-5 sm:p-6">
	<h2 class="mb-5 text-base font-bold text-gray-900">Entered Results</h2>

	{#each resultsObj?.results ?? [] as eventResult (eventResult.event)}
		{@const eventAttempts = getAttemptCount(eventResult.event)}
		<div class="mb-6 last:mb-0">
			<div class="mb-3 flex items-center gap-2 border-b border-gray-200 pb-2">
				<CubeIcon event={eventResult.event} class="text-base text-uoft-blue" />
				<h3 class="text-sm font-bold text-gray-900">{eventNames[eventResult.event]}</h3>
			</div>

			{#each eventResult.rounds as round (round.round)}
				{#if round.results.length > 0}
					<div class="mb-5">
						<h4 class="mb-2 text-xs font-semibold tracking-wider text-gray-700 uppercase">
							Round {round.round}
						</h4>
						<div class="overflow-x-auto border border-gray-200">
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
								<thead class="bg-gray-50">
									<tr class="border-b border-gray-200">
										<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>Name</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>T1</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>T2</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>T3</th
										>
										{#if eventAttempts == 5}
											<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
												>T4</th
											>
											<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
												>T5</th
											>
										{/if}
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>Single</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-uoft-blue uppercase"
											>{getMeanType(eventResult.event)}</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>Actions</th
										>
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-100 bg-white">
									{#each round.results as personResult, idx (idx)}
										{@const result = convertToResult(
											personResult,
											eventResult.event,
											round.round,
											resultsObj!.competition.id,
										)}
										<tr class="transition-colors hover:bg-gray-50/50">
											<td class="truncate px-4 py-2 text-sm font-medium text-gray-900">{personResult.person_name}</td>
											<td class="px-4 py-2 text-right font-mono text-sm text-gray-700 tabular-nums"
												>{renderTime(personResult.times[0] || 0)}</td
											>
											<td class="px-4 py-2 text-right font-mono text-sm text-gray-700 tabular-nums"
												>{renderTime(personResult.times[1] || 0)}</td
											>
											<td class="px-4 py-2 text-right font-mono text-sm text-gray-700 tabular-nums"
												>{renderTime(personResult.times[2] || 0)}</td
											>
											{#if eventAttempts == 5}
												<td class="px-4 py-2 text-right font-mono text-sm text-gray-700 tabular-nums"
													>{renderTime(personResult.times[3] || 0)}</td
												>
												<td class="px-4 py-2 text-right font-mono text-sm text-gray-700 tabular-nums"
													>{renderTime(personResult.times[4] || 0)}</td
												>
											{/if}
											<td class="px-4 py-2 text-right font-mono text-sm font-semibold text-gray-900 tabular-nums">
												{renderTime(personResult.single)}
											</td>
											<td
												class="bg-uoft-blue/[0.04] px-4 py-2 text-right font-mono text-sm font-bold text-uoft-blue tabular-nums"
											>
												{renderTime(personResult.average)}
											</td>
											<td class="px-4 py-2 text-right">
												<div class="inline-flex items-center justify-end gap-1.5">
													<button
														type="button"
														onclick={() => onEdit(result)}
														class="cursor-pointer rounded-sm border border-gray-200 bg-white px-2 py-0.5 text-xs font-medium text-gray-700 transition-colors hover:border-uoft-blue hover:bg-gray-50"
													>
														Edit
													</button>
													<button
														type="button"
														onclick={() => onDelete(personResult.id)}
														class="cursor-pointer rounded-sm border border-red-200 bg-white px-2 py-0.5 text-xs font-medium text-uoft-warm-red transition-colors hover:bg-red-50"
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
		<p class="py-8 text-center text-xs text-gray-700">No results submitted yet.</p>
	{/each}
</div>
