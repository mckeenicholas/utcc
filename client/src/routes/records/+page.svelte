<script lang="ts">
import { onMount } from "svelte";
import Backbutton from "$lib/components/Backbutton.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import RecordRow from "$lib/components/RecordRow.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import UofTSelector from "$lib/components/UofTSelector.svelte";
import {
	type EventRecords,
	type Session,
	type StudentStatus,
	type WCAEvent,
	eventNames,
	eventSolves,
} from "$lib/types";
import { BASE_URL, fetchJson, processPersonalRecords, sortEvents } from "$lib/utils";

let sessions: Session[] = $state([]);
let selectedSession: string = $state("-1");
let studentStatus: StudentStatus = $state([]);
let recordsAPIResponse: Record<string, EventRecords> = $state({});
let loading = $state(true);
let innerWidth = $state<number>(0);

onMount(async () => {
	try {
		const fetchedSessions = await fetchJson<Session[]>(`${BASE_URL}/api/session/`);
		sessions = fetchedSessions;
	} catch (error) {
		console.error("Error fetching sessions:", error);
	}
});

$effect(() => {
	const fetchRecords = async () => {
		loading = true;
		try {
			const url = new URL(`${BASE_URL}/api/records/`);
			if (selectedSession !== "-1") {
				url.searchParams.set("session_id", selectedSession);
			}
			if (studentStatus.length > 0) {
				studentStatus.forEach((status) => {
					url.searchParams.append("uoft", status);
				});
			}

			const records = await fetchJson<Record<string, EventRecords>>(url);
			recordsAPIResponse = records;
		} catch (error) {
			console.error("Error loading records:", error);
		} finally {
			loading = false;
		}
	};

	fetchRecords();
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

<svelte:window bind:innerWidth />

<svelte:head>
	<title>UofT Rubik's Cube Club Records</title>
	<meta name="description" content="Current records from University of Toronto Rubik's Cube Club." />
</svelte:head>

<Backbutton />

<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
		<!-- Header & Filters -->
		<div class="mb-8 flex flex-col gap-6 md:flex-row md:items-center md:justify-between">
			<div>
				<h1 class="text-3xl font-extrabold tracking-tight text-gray-900">Club Records</h1>
				<p class="mt-2 text-base text-gray-600">Fastest results set at club-sanctioned competitions.</p>
			</div>
			<div
				class="flex flex-col items-stretch gap-4 rounded-xl border border-gray-200 bg-white p-3 shadow-sm sm:flex-row sm:items-center"
			>
				<div class="flex items-center gap-2">
					<span class="text-sm font-bold whitespace-nowrap text-gray-700">Session:</span>
					<SessionSelector bind:value={selectedSession} sessionData={sessions} class="shadow-sm" />
				</div>
				<div class="flex items-center gap-2 border-t border-gray-100 pt-3 sm:border-t-0 sm:pt-0">
					<span class="text-sm font-bold whitespace-nowrap text-gray-700">Status:</span>
					<UofTSelector bind:status={studentStatus} vertical={innerWidth < 430} />
				</div>
			</div>
		</div>

		{#if loading}
			<div class="flex min-h-[300px] items-center justify-center">
				<LoadingScreen message="Loading Records" inline />
			</div>
		{:else if recordsDisplay.length > 0}
			<div class="space-y-6">
				{#each recordsDisplay as [eventKey, eventRecords] (eventKey)}
					<div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
						<div class="border-b border-gray-100 bg-gray-50/50 px-6 py-4">
							<h2 class="text-lg font-bold text-gray-900">{eventNames[eventKey]}</h2>
						</div>
						<div class="overflow-x-auto">
							<table class="min-w-full divide-y divide-gray-200">
								<thead class="bg-gray-50/50">
									<tr>
										<th class="px-6 py-3 text-left text-xs font-semibold tracking-wider text-gray-500 uppercase"
											>Type</th
										>
										<th class="px-6 py-3 text-left text-xs font-semibold tracking-wider text-gray-500 uppercase"
											>Name</th
										>
										<th class="px-6 py-3 text-left text-xs font-semibold tracking-wider text-gray-500 uppercase"
											>Competition</th
										>
										<th class="px-6 py-3 text-center text-xs font-semibold tracking-wider text-gray-500 uppercase"
											>Result</th
										>
										{#each Array.from({ length: eventSolves[eventKey]! }).keys() as idx (idx)}
											<th
												class="hidden px-6 py-3 text-center text-xs font-semibold tracking-wider text-gray-500 uppercase md:table-cell"
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
			<div class="rounded-xl border border-gray-200 bg-white p-12 text-center shadow-sm">
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
				<h3 class="mt-4 text-lg font-bold text-gray-900">No Records Available</h3>
				<p class="mt-2 text-sm font-medium text-gray-500">There are no club records to display at this time.</p>
			</div>
		{/if}
	</div>
</div>
