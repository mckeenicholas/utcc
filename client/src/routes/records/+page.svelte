<script lang="ts">
import type {
	EventRecords,
	RecordsApiResponse,
	Session,
	StudentStatus,
	WCAEvent
} from '$lib/types';
import { fetchJson, recordsURL, sortEvents } from '$lib/utils';
import { eventSolves, eventNames } from '$lib/types';
import { onMount } from 'svelte';
import RecordRow from '$lib/components/RecordRow.svelte';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import SessionSelector from '$lib/components/SessionSelector.svelte';
import { fetchSessions } from '$lib/competitionSessionService';
import UofTSelector from '$lib/components/UofTSelector.svelte';

let recordsAPIResponse: RecordsApiResponse | null = $state(null);
let selectedSession: string = $state('-1');
let studentStatus: StudentStatus = $state('all');
let sessions: Session[] = $state([]);
let loading = $state(true);

let innerWidth = $state(0);

const sessionRecordsURL = (sessionId: number, uoftStatus: StudentStatus) => {
	const url = new URL(recordsURL);
	if (sessionId !== -1) url.searchParams.set('session_id', sessionId.toString());

	if (uoftStatus == 'uoft') {
		url.searchParams.set('uoft', '1');
	} else if (uoftStatus == 'non-uoft') {
		url.searchParams.set('uoft', '0');
	}

	return url;
};

$effect(() => {
	fetchRecords(parseInt(selectedSession), studentStatus);
});

const fetchRecords = async (sessionId: number, uoftStatus: StudentStatus) => {
	try {
		loading = true;
		recordsAPIResponse = await fetchJson<RecordsApiResponse>(
			sessionRecordsURL(sessionId, uoftStatus)
		);
	} catch (error) {
		console.error('Failed to fetch records:', error);
	} finally {
		loading = false;
	}
};

onMount(async () => {
	sessions = await fetchSessions();
});

let recordsDisplay = $derived.by(() => {
	if (!recordsAPIResponse) {
		return [];
	}

	const recordEntries = Object.entries(recordsAPIResponse) as [WCAEvent, EventRecords][];
	recordEntries.sort((a, b) => sortEvents(a[0] as WCAEvent, b[0] as WCAEvent));
	return recordEntries;
});
</script>

<svelte:window bind:innerWidth={innerWidth} />

<svelte:head>
	<title>UofT Rubik's Cube Club Records</title>
	<meta
		name="description"
		content="Current records from University of Toronto Rubik's Cube Club."
	/>
</svelte:head>

<Backbutton />

<div class="min-h-screen py-8">
	<div class="mx-4 max-w-6xl">
		<div class="mb-8 flex items-start justify-between">
			<div>
				<h1 class="text-3xl font-bold text-gray-900">Club Records</h1>
				<p class="mt-2 text-gray-600">Fastest result set at a club-sanctioned competition</p>
			</div>
			<div
				class="ms-2 flex flex-col items-center gap-4 rounded-lg border border-gray-200 bg-white p-2 shadow-sm sm:flex-row"
			>
				<SessionSelector bind:value={selectedSession} sessionData={sessions} class="shadow-sm" />
				<UofTSelector bind:status={studentStatus} vertical={innerWidth < 430} />
			</div>
		</div>
		{#if loading}
			<LoadingScreen message="Loading Records" inline />
		{:else if recordsDisplay.length > 0}
			<div class="space-y-6">
				{#each recordsDisplay as [eventKey, eventRecords] (eventKey)}
					<div class="overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
						<div class="rounded-t-lg border-b border-gray-200 px-4 py-2">
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
									{#if eventRecords.single}
										<RecordRow record={eventRecords.single} eventKey={eventKey} type="Single" />
									{/if}
									{#if eventRecords.average}
										<RecordRow record={eventRecords.average} eventKey={eventKey} type="Average" />
									{/if}
								</tbody>
							</table>
						</div>
					</div>
				{/each}
			</div>
		{:else}
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
		{/if}
	</div>
</div>
