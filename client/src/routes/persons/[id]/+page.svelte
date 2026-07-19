<script lang="ts">
import { page } from "$app/stores";
import Backbutton from "$lib/components/Backbutton.svelte";
import CompetitionResultsTable from "$lib/components/CompetitionResultsTable.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PersonalRecordsTable from "$lib/components/PersonalRecordsTable.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import { type ProfileResponse, type Session, type UserProfileResponse, type WCAEvent } from "$lib/types";
import { BASE_URL, fetchJson, generateRecordsForEvent, processPersonalRecords } from "$lib/utils";

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
		Results for {profileResults?.name ?? "competitor"}
	</title>
</svelte:head>

<Backbutton />
<div class="min-h-screen bg-gray-50 py-8">
	{#if error}
		<div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
			<div class="rounded-xl border border-gray-200 bg-white p-8 text-center shadow-sm">
				<h3 class="text-lg font-bold text-gray-900">{error}</h3>
			</div>
		</div>
	{:else if loading}
		<div class="flex min-h-[300px] items-center justify-center">
			<LoadingScreen message="Loading Profile" inline minHeight="30rem" />
		</div>
	{:else}
		<div class="mx-auto w-full max-w-6xl space-y-6 px-4 sm:px-6 lg:px-8">
			<!-- Header -->
			<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
				<div>
					<h1 class="text-3xl font-extrabold tracking-tight text-gray-900">{profileResults!.name}</h1>
					<p class="mt-2 text-base text-gray-600">Competition Profile</p>
				</div>
				{#if allSessions.length}
					<div
						class="flex items-center gap-2 self-start rounded-xl border border-gray-200 bg-white p-2.5 shadow-sm sm:self-auto"
					>
						<span class="text-sm font-bold whitespace-nowrap text-gray-700">Session:</span>
						<SessionSelector bind:value={selectedSession} sessionData={allSessions} class="shadow-sm" />
					</div>
				{/if}
			</div>

			<!-- Personal Records -->
			{#if profileResults?.records.length}
				<div class="w-full">
					<PersonalRecordsTable records={profileResults.records} />
				</div>
			{/if}

			<!-- Competition Results -->
			<div class="w-full">
				<CompetitionResultsTable results={profileResults!.results} {selectedEvent} />
			</div>
		</div>
	{/if}
</div>
