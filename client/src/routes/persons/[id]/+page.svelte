<script lang="ts">
import { page } from "$app/stores";
import CompetitionResultsTable from "$lib/components/CompetitionResultsTable.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PersonalRecordsTable from "$lib/components/PersonalRecordsTable.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import { type ProfileResponse, type Session, type UserProfileResponse, type WCAEvent } from "$lib/types";
import { BASE_URL, fetchJson, generateRecordsForEvent, processPersonalRecords, sortEvents } from "$lib/utils";

const personId = $page.params.id;
let selectedEvent: WCAEvent = $state("333");
let selectedSession: string = $state("-1");
let profileResults = $state<UserProfileResponse | null>(null);
let allSessions: Session[] = $state([]);
let loading = $state(true);
let error = $state("");

const fetchProfileResults = async (session_id: string) => {
	try {
		const url = new URL(`${BASE_URL}/api/users/${personId}/results/`);

		if (session_id !== "-1") {
			url.searchParams.append("session_id", session_id);
		}

		const response = await fetchJson<ProfileResponse>(url);

		allSessions = response.person.sessions;

		const personalRecords = processPersonalRecords(response.records);
		const resultsTableContent = response.results.map(generateRecordsForEvent);

		profileResults = {
			name: response.person.name,
			records: personalRecords,
			results: resultsTableContent,
		} as unknown as UserProfileResponse;

		const availableEvents = resultsTableContent.map((r) => r.event).toSorted(sortEvents);
		if (availableEvents.length > 0 && !availableEvents.includes(selectedEvent)) {
			selectedEvent = availableEvents.includes("333") ? "333" : availableEvents[0];
		}
	} catch {
		error = "Unable to fetch user profile.";
	} finally {
		loading = false;
	}
};

$effect(() => {
	fetchProfileResults(selectedSession);
});
</script>

<svelte:head>
	<title>
		{profileResults?.name ? `${profileResults.name} | Results` : "Competitor Profile"} | U of T Cube Club
	</title>
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		{#if error}
			<div class="border border-red-200 bg-white p-8 text-center sm:p-12">
				<div class="mx-auto flex h-10 w-10 items-center justify-center rounded-sm bg-red-50 text-uoft-warm-red">
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="mt-3 text-base font-bold text-gray-900">{error}</h3>
				<p class="mt-1 text-xs text-gray-700">Could not retrieve competitor data from the server.</p>
			</div>
		{:else if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen message="Loading Profile..." inline minHeight="15rem" />
			</div>
		{:else if profileResults}
			<!-- Header -->
			<div class="mb-6">
				<div class="flex items-center gap-2">
					<a href="/persons" class="text-xs font-semibold text-uoft-blue hover:underline">&larr; All Competitors</a>
				</div>
				<h1 class="mt-1 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
					{profileResults.name}
				</h1>
				<p class="mt-1 text-sm text-gray-700">Member Competition Profile & Solves</p>
			</div>

			{#if allSessions.length}
				<!-- Filter Toolbar -->
				<div class="mb-6 flex flex-wrap items-center gap-3 border border-gray-200 bg-white p-4 sm:p-5">
					<span class="text-xs font-semibold tracking-wider text-gray-700 uppercase">Session:</span>
					<SessionSelector bind:value={selectedSession} sessionData={allSessions} />
				</div>
			{/if}

			<!-- Personal Records -->
			{#if profileResults.records.length}
				<div class="mb-6">
					<PersonalRecordsTable records={profileResults.records} />
				</div>
			{/if}

			<!-- Competition Results -->
			<div>
				<CompetitionResultsTable results={profileResults.results} bind:selectedEvent />
			</div>
		{/if}
	</div>
</div>
