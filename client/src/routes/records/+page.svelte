<script lang="ts">
import type { EventRecords, RecordsApiResponse, WCAEvent } from '$lib/types';
import { recordsURL } from '$lib/utils';
import { eventListIdx, eventSolves, eventNames } from '$lib/types';
import RecordRow from '$lib/components/RecordRow.svelte';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import { createQuery } from '@tanstack/svelte-query';

const fetchRecords = async () => {
	const response = await fetch(recordsURL);
	const data: RecordsApiResponse = await response.json();

	const recordEntries = Object.entries(data) as [WCAEvent, EventRecords][];
	recordEntries.sort((a, b) => {
		const eventA = a[0] as WCAEvent;
		const eventB = b[0] as WCAEvent;
		return eventListIdx[eventA] - eventListIdx[eventB];
	}) as [WCAEvent, EventRecords][];

	return recordEntries;
};

const query = createQuery({ queryKey: ['records'], queryFn: fetchRecords });
</script>

<Backbutton />
{#if $query.isSuccess && $query.data}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-6xl px-4">
			<!-- Header -->
			<div class="mb-8">
				<h1 class="text-3xl font-bold text-gray-900">Club Records</h1>
				<p class="mt-2 text-gray-600">Fastest result set at a club-sanctioned competition</p>
			</div>

			<div class="space-y-6">
				{#each $query.data as [eventKey, eventRecords] (eventKey)}
					<div class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
						<div class=" rounded-t-lg border-b border-gray-200 px-4 py-2">
							<h2 class="text-lg font-semibold text-gray-800">{eventNames[eventKey]}</h2>
						</div>
						<div class="overflow-x-auto">
							<table class="min-w-full divide-y divide-gray-200">
								<thead>
									<tr>
										<th
											class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Type</th
										>
										<th
											class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Name</th
										>
										<th
											class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Competition</th
										>
										<th
											class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
											>Result</th
										>
										{#each Array.from({ length: eventSolves[eventKey]! }).keys() as idx (idx)}
											<th
												class="hidden px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase md:table-cell"
											>
												Solve {idx + 1}
											</th>
										{/each}
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-200 bg-white">
									<RecordRow record={eventRecords.single} eventKey={eventKey} type="Single" />
									<RecordRow record={eventRecords.average} eventKey={eventKey} type="Average" />
								</tbody>
							</table>
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
{:else if $query.isSuccess}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-6xl px-4">
			<div class="rounded-lg bg-white p-6 text-center shadow-sm">
				<div class="mx-auto h-12 w-12 text-gray-400">
					<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
						/>
					</svg>
				</div>
				<h3 class="mt-4 text-lg font-medium text-gray-900">No Records Available</h3>
				<p class="mt-2 text-gray-600">There are no club records to display at this time.</p>
			</div>
		</div>
	</div>
{:else}
	<LoadingScreen message="Loading Records" />
{/if}
