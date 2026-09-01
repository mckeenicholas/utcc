<script lang="ts">
import { onMount } from "svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import RecordRow from "$lib/components/RecordRow.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import UofTSelector from "$lib/components/UofTSelector.svelte";
import { fetchSessions } from "$lib/competitionSessionService";
import {
	eventNames,
	eventSolves,
	type EventRecords,
	type RecordsApiResponse,
	type Session,
	type StudentStatus,
	type WCAEvent,
} from "$lib/types";
import { fetchJson, recordsURL, sortEvents, toInt } from "$lib/utils";

let recordsAPIResponse: RecordsApiResponse | null = $state(null);
let selectedSession: string = $state("-1");
let studentStatus: StudentStatus = $state([]);
let sessions: Session[] = $state([]);
let loading = $state(true);

const sessionRecordsURL = (sessionId: number, uoftStatus: StudentStatus) => {
	const url = new URL(recordsURL);
	if (sessionId !== -1) {
		url.searchParams.set("session_id", sessionId.toString());
	}

	if (uoftStatus.length > 0) {
		uoftStatus.forEach((status) => {
			url.searchParams.append("uoft", status);
		});
	}

	return url;
};

$effect(() => {
	fetchRecords(toInt(selectedSession) ?? -1, studentStatus);
});

const fetchRecords = async (sessionId: number, uoftStatus: StudentStatus) => {
	try {
		loading = true;
		recordsAPIResponse = await fetchJson<RecordsApiResponse>(sessionRecordsURL(sessionId, uoftStatus));
	} catch (error) {
		console.error("Failed to fetch records:", error);
	} finally {
		loading = false;
	}
};

onMount(async () => {
	sessions = await fetchSessions();
});

const recordsDisplay = $derived.by(() => {
	if (!recordsAPIResponse) {
		return [];
	}

	const recordEntries = Object.entries(recordsAPIResponse) as [WCAEvent, EventRecords][];
	recordEntries.sort((a, b) => sortEvents(a[0] as WCAEvent, b[0] as WCAEvent));
	return recordEntries;
});
</script>

<svelte:head>
	<title>Club Records | University of Toronto Cube Club</title>
	<meta name="description" content="Current records from University of Toronto Rubik's Cube Club." />
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<!-- Header -->
		<div class="mb-6">
			<h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Club Records</h1>
			<p class="mt-1 text-sm text-gray-700">Fastest official times set at club-sanctioned competitions.</p>
		</div>

		<!-- Filter Toolbar -->
		<div class="mb-6 flex flex-wrap items-center gap-4 border border-gray-200 bg-white p-4 sm:p-5">
			<span class="text-xs font-semibold tracking-wider text-gray-700 uppercase">Filter:</span>
			<div class="flex items-center gap-2">
				<span class="text-xs font-medium text-gray-700">Session:</span>
				<SessionSelector bind:value={selectedSession} sessionData={sessions} />
			</div>
			<div class="flex items-center gap-2">
				<span class="text-xs font-medium text-gray-700">Status:</span>
				<UofTSelector bind:status={studentStatus} />
			</div>
		</div>

		{#if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen message="Loading Records..." inline />
			</div>
		{:else if recordsDisplay.length > 0}
			<div class="space-y-6">
				{#each recordsDisplay as [eventKey, eventRecords] (eventKey)}
					<div class="overflow-hidden border border-gray-200 bg-white">
						<div class="flex items-center gap-2.5 border-b border-gray-200 bg-gray-50 px-4 py-2.5 sm:px-5">
							<span class="cubing-icon event-{eventKey} text-base text-uoft-blue"></span>
							<h2 class="text-sm font-bold tracking-tight text-gray-900">{eventNames[eventKey]}</h2>
						</div>
						<div class="overflow-x-auto">
							<table class="min-w-full divide-y divide-gray-200">
								<thead class="bg-gray-50">
									<tr>
										<th class="w-24 px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>Type</th
										>
										<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>Name</th
										>
										<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase"
											>Competition</th
										>
										<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-uoft-blue uppercase"
											>Result</th
										>
										{#each Array.from({ length: eventSolves[eventKey]! }).keys() as idx (idx)}
											<th
												class="hidden px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase md:table-cell"
											>
												Solve {idx + 1}
											</th>
										{/each}
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-100 bg-white">
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
		{:else}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-sm bg-gray-100 text-gray-700">
					<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
						/>
					</svg>
				</div>
				<h3 class="mt-3 text-base font-bold text-gray-900">No Records Found</h3>
				<p class="mt-1 text-xs text-gray-700">There are no records matching the selected session or status filter.</p>
			</div>
		{/if}
	</div>
</div>
