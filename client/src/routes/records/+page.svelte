<script lang="ts">
	import type { EventRecords, RecordsApiResponse, WCAEvent } from '$lib/types';
	import { recordsURL } from '$lib/utils';
	import { eventListIdx, eventSolves, eventNames } from '$lib/types';
	import { onMount } from 'svelte';
	import RecordRow from '$lib/components/RecordRow.svelte';

	let recordsAPIResponse = $state<RecordsApiResponse | null>(null);

	onMount(async () => {
		const response = await fetch(recordsURL);
		const data: RecordsApiResponse = await response.json();

		recordsAPIResponse = data;
	});

	let recordsDisplay = $derived.by(() => {
		if (!recordsAPIResponse) {
			return null;
		}

		const recordEntries = Object.entries(recordsAPIResponse) as [WCAEvent, EventRecords][];
		recordEntries.sort((a, b) => {
			const eventA = a[0] as WCAEvent;
			const eventB = b[0] as WCAEvent;
			return eventListIdx[eventA] - eventListIdx[eventB];
		}) as [WCAEvent, EventRecords][];

		return recordEntries;
	});
</script>

<div class="m-4 mb-3">
	<a class="rounded-md bg-gray-200 p-2 text-xl hover:bg-gray-300" href="/results"> ← Back </a>
</div>
{#if recordsDisplay}
	<div class="mx-4 my-2">
		<h1 class="mb-4 text-2xl font-bold">Club Records</h1>
		<div class="w-full space-y-6">
			{#each recordsDisplay as [eventKey, eventRecords] (eventKey)}
				<div class="rounded-lg bg-white p-1 shadow">
					<h2 class="mb-2 ms-2 text-xl font-semibold">{eventNames[eventKey]}</h2>
					<div class="overflow-x-auto rounded-md">
						<table class="w-full">
							<thead class="bg-gray-200">
								<tr>
									<th class="px-4 py-2 text-center">Type</th>
									<th class="px-4 py-2 text-center">Name</th>
									<th class="px-4 py-2 text-center">Competition</th>
									<th class="px-4 py-2 text-center">Result</th>
									{#each Array.from({ length: eventSolves[eventKey]! }).keys() as idx (idx)}
										<th class="hidden px-4 py-2 text-center md:table-cell">{idx + 1}</th>
									{/each}
								</tr>
							</thead>
							<tbody class="bg-gray-100">
								{#if eventRecords.single}
									<RecordRow record={eventRecords.single} {eventKey} type="Single" />
								{/if}
								{#if eventRecords.average}
									<RecordRow record={eventRecords.average} {eventKey} type="Average" />
								{/if}
							</tbody>
						</table>
					</div>
				</div>
			{/each}
		</div>
	</div>
{/if}
