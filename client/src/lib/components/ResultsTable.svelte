<script lang="ts">
	import type { Result, WCAEvent } from '$lib/types';
	import { eventNames, eventSolves } from '$lib/types';
	import { getMeanType, renderTime } from '$lib/utils';

	interface Props {
		results: Result[];
		onEdit: (result: Result) => void;
		onDelete: (resultId: number) => void;
	}

	let { results, onEdit, onDelete }: Props = $props();

	// Computed property for number of attempts
	const getAttemptCount = (event: WCAEvent): number => {
		return eventSolves[event] || 5;
	};
</script>

<div class="rounded-lg bg-white p-6 shadow-sm">
	<h2 class="mb-6 text-xl font-semibold text-gray-800">Results</h2>

	{#if results.length === 0}
		<p class="py-8 text-center text-gray-500">No results submitted yet.</p>
	{:else}
		{#each Object.entries(eventNames) as [eventKey, eventName] (eventKey)}
			{@const eventResults = results.filter((r) => r.event === eventKey)}
			{@const eventAttempts = getAttemptCount(eventKey as WCAEvent)}
			{#if eventResults.length > 0}
				<div class="mb-8">
					<h3 class="mb-4 text-lg font-semibold text-gray-800">{eventName}</h3>

					{#each [1, 2, 3, 4, 5] as round (round)}
						{@const roundResults = eventResults.filter((r) => r.round === round)}
						{#if roundResults.length > 0}
							<div class="mb-6 ms-4">
								<h4 class="text-md mb-3 font-medium text-gray-700">Round {round}</h4>
								<div class="overflow-x-auto">
									<table class="w-full table-fixed border-collapse">
										<colgroup>
											<col class="w-32" />
											<!-- Name -->
											<col class="w-20" />
											<!-- Time 1 -->
											<col class="w-20" />
											<!-- Time 2 -->
											<col class="w-20" />
											<!-- Time 3 -->
											<col class="w-20" />
											<!-- Time 4 -->
											<col class="w-20" />
											<!-- Time 5 -->
											<col class="w-24" />
											<!-- Single -->
											<col class="w-24" />
											<!-- Average/Mean -->
											<col class="w-28" />
											<!-- Actions -->
										</colgroup>
										<thead>
											<tr class="border-b border-gray-200">
												<th class="px-4 py-3 text-left text-sm font-medium text-gray-700">Name</th>
												<th class="px-4 py-3 text-right text-sm font-medium text-gray-700"
													>Time 1</th
												>
												<th class="px-4 py-3 text-right text-sm font-medium text-gray-700"
													>Time 2</th
												>
												<th class="px-4 py-3 text-right text-sm font-medium text-gray-700"
													>Time 3</th
												>
												<th
													class="px-4 py-3 text-right text-sm font-medium text-gray-700 {eventAttempts ===
													3
														? 'text-gray-300'
														: ''}">Time 4</th
												>
												<th
													class="px-4 py-3 text-right text-sm font-medium text-gray-700 {eventAttempts ===
													3
														? 'text-gray-300'
														: ''}">Time 5</th
												>
												<th class="px-4 py-3 text-right text-sm font-medium text-gray-700"
													>Single</th
												>
												<th class="px-4 py-3 text-right text-sm font-medium text-gray-700"
													>{getMeanType(eventKey as WCAEvent)}</th
												>
												<th class="px-4 py-3 text-left text-sm font-medium text-gray-700"
													>Actions</th
												>
											</tr>
										</thead>
										<tbody>
											{#each roundResults as result, idx (idx)}
												<tr class="hover: border-b border-gray-100">
													<td class="px-4 py-3 text-sm text-gray-900">{result.name}</td>
													<td class="px-4 py-3 text-right text-sm text-gray-900"
														>{renderTime(result.time1)}</td
													>
													<td class="px-4 py-3 text-right text-sm text-gray-900"
														>{renderTime(result.time2)}</td
													>
													<td class="px-4 py-3 text-right text-sm text-gray-900"
														>{renderTime(result.time3)}</td
													>
													<td
														class="px-4 py-3 text-sm {eventAttempts === 3
															? 'text-gray-300'
															: 'text-gray-900'} text-right"
														>{eventAttempts === 5 ? renderTime(result.time4) : '-'}</td
													>
													<td
														class="px-4 py-3 text-sm {eventAttempts === 3
															? 'text-gray-300'
															: 'text-gray-900'} text-right"
														>{eventAttempts === 5 ? renderTime(result.time5) : '-'}</td
													>
													<td
														class="bg-green-50 px-4 py-3 text-right text-sm font-semibold text-green-700"
														>{renderTime(result.single)}</td
													>
													<td
														class="bg-blue-50 px-4 py-3 text-right text-sm font-semibold text-blue-700"
														>{renderTime(result.average)}</td
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
																onclick={() => onDelete(result.id)}
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
			{/if}
		{/each}
	{/if}
</div>
