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
			.map((event) => ({
				...event,
				rounds: event.rounds
					.map((round) => ({
						...round,
						results: [...round.results].toSorted(compareResults),
					}))
					.toSorted((a, b) => a.round - b.round),
			}))
			.toSorted((a, b) => sortEvents(a.event, b.event)),
	};
});

const getAttemptCount = (event: WCAEvent): number => eventSolves[event] || 5;

const convertToResult = (personResult: PersonResult, event: WCAEvent, round: number, compId: number): Result => ({
	average: personResult.average,
	competition: compId,
	event,
	id: personResult.id,
	person: personResult.person,
	person_name: personResult.person_name,
	round,
	single: personResult.single,
	time1: personResult.times[0] || 0,
	time2: personResult.times[1] || 0,
	time3: personResult.times[2] || 0,
	time4: personResult.times[3] || 0,
	time5: personResult.times[4] || 0,
});
</script>

<div class="rounded-lg bg-white p-6 shadow-sm">
	<h2 class="mb-6 text-xl font-semibold text-gray-800">Results</h2>

	{#each resultsObj?.results ?? [] as eventResult (eventResult.event)}
		{@const eventAttempts = getAttemptCount(eventResult.event)}
		<div class="mb-8">
			<h3 class="mb-4 text-lg font-semibold text-gray-800">{eventNames[eventResult.event]}</h3>

			{#each eventResult.rounds as round (round.round)}
				{#if round.results.length > 0}
					<div class="ms-4 mb-6">
						<h4 class="text-md mb-3 font-medium text-gray-700">Round {round.round}</h4>
						<div class="overflow-x-auto">
							<table class="w-full table-fixed border-collapse">
								<colgroup>
									<col class="w-32" />
									<col class="w-20" /> <col class="w-20" /> <col class="w-20" />
									{#if eventAttempts == 5}
										<col class="w-20" />
										<col class="w-20" />
									{/if}
									<col class="w-24" />
									<col class="w-24" />
									<col class="w-28" />
								</colgroup>
								<thead>
									<tr class="border-b border-gray-200">
										<th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Name</th>
										<th class="px-4 py-3 text-right text-sm font-medium text-gray-700">Time 1</th>
										<th class="px-4 py-3 text-right text-sm font-medium text-gray-700">Time 2</th>
										<th class="px-4 py-3 text-right text-sm font-medium text-gray-700">Time 3</th>
										{#if eventAttempts == 5}
											<th class="px-4 py-3 text-right text-sm font-medium text-gray-700">Time 4</th>
											<th class="px-4 py-3 text-right text-sm font-medium text-gray-700">Time 5</th>
										{/if}
										<th class="px-4 py-3 text-right text-sm font-medium text-gray-700">Single</th>
										<th class="px-4 py-3 text-right text-sm font-medium text-gray-700"
											>{getMeanType(eventResult.event)}</th
										>
										<th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Actions</th>
									</tr>
								</thead>
								<tbody>
									{#each round.results as personResult, idx (idx)}
										{@const result = convertToResult(
											personResult,
											eventResult.event,
											round.round,
											resultsObj!.competition.id,
										)}
										<tr class="hover: border-b border-gray-100">
											<td class="px-4 py-3 text-sm text-gray-900">{personResult.person_name}</td>
											<td class="px-4 py-3 text-right text-sm text-gray-900"
												>{renderTime(personResult.times[0] || 0)}</td
											>
											<td class="px-4 py-3 text-right text-sm text-gray-900"
												>{renderTime(personResult.times[1] || 0)}</td
											>
											<td class="px-4 py-3 text-right text-sm text-gray-900"
												>{renderTime(personResult.times[2] || 0)}</td
											>
											{#if eventAttempts == 5}
												<td class="px-4 py-3 text-right text-sm text-gray-900"
													>{renderTime(personResult.times[3] || 0)}</td
												>
												<td class="px-4 py-3 text-right text-sm text-gray-900"
													>{renderTime(personResult.times[4] || 0)}</td
												>
											{/if}
											<td class="bg-green-50 px-4 py-3 text-right text-sm font-semibold text-green-700"
												>{renderTime(personResult.single)}</td
											>
											<td class="bg-blue-50 px-4 py-3 text-right text-sm font-semibold text-blue-700"
												>{renderTime(personResult.average)}</td
											>
											<td class="px-4 py-3">
												<div class="flex space-x-2">
													<button
														onclick={() => onEdit(result)}
														class="inline-flex items-center rounded bg-yellow-100 px-2 py-1 text-xs font-medium text-yellow-800 hover:bg-yellow-200"
													>
														Edit
													</button>
													<button
														onclick={() => onDelete(personResult.id)}
														class="inline-flex items-center rounded bg-red-100 px-2 py-1 text-xs font-medium text-red-800 hover:bg-red-200"
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
		<p class="py-8 text-center text-gray-500">No results submitted yet.</p>
	{/each}
</div>
