<script lang="ts">
import { page } from '$app/stores';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import PersonalRecordsTable from '$lib/components/PersonalRecordsTable.svelte';
import CompetitionResultsTable from '$lib/components/CompetitionResultsTable.svelte';
import {
	type ProfileResponse,
	type Session,
	type UserProfileResponse,
	type WCAEvent
} from '$lib/types';
import { BASE_URL, processPersonalRecords, generateRecordsForEvent, fetchJson } from '$lib/utils';
import SessionSelector from '$lib/components/SessionSelector.svelte';

const personId = $page.params.id;
let selectedEvent: WCAEvent = $state('333');
let selectedSession: string = $state('-1');
let profileResults = $state<UserProfileResponse | null>(null);
let allSessions: Session[] = $state([]);
let loading = $state(true);
let error = $state('');

const fetchProfileResults = async (session_id: string) => {
	try {
		const url = new URL(`${BASE_URL}/api/users/${personId}/results/`);

		if (session_id !== '-1') url.searchParams.append('session_id', session_id);

		const response = await fetchJson<ProfileResponse>(url);

		allSessions = response.person.sessions;

		const personalRecords = processPersonalRecords(response.records);
		const resultsTableContent = response.results.map(generateRecordsForEvent);

		profileResults = {
			records: personalRecords,
			results: resultsTableContent,
			name: response.person.name
		} as unknown as UserProfileResponse;
	} catch (err) {
		console.log('Error fetching user profile', err);
		error = 'Unable to fetch user profile.';
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
<div class="flex bg-gray-50 py-8">
	{#if error}
		<div class="mx-auto max-w-6xl px-4">
			<div class="rounded-lg bg-white p-8 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">{error}</h3>
			</div>
		</div>
	{:else if loading}
		<div class="flex min-h-120 w-full items-center justify-center">
			<LoadingScreen message="Loading Profile" inline minHeight="30rem" />
		</div>
	{:else}
		<div class="mx-auto max-w-6xl px-4">
			<!-- Header -->
			<div class="flex items-start justify-between">
				<div class="mb-8">
					<h1 class="text-3xl font-bold text-gray-900">{profileResults!.name}</h1>
					<p class="mt-2 text-gray-600">Competition Profile</p>
				</div>
				{#if allSessions.length}
					<SessionSelector
						bind:value={selectedSession}
						sessionData={allSessions}
						class="mt-2 shadow-sm"
					/>
				{/if}
			</div>

			<!-- Personal Records -->
			{#if profileResults?.records.length}
				<div class="w-full min-w-[600px]">
					<PersonalRecordsTable records={profileResults.records} />
				</div>
			{/if}

			<!-- Competition Results -->
			<div class="w-full min-w-[900px]">
				<CompetitionResultsTable results={profileResults!.results} selectedEvent={selectedEvent} />
			</div>
		</div>
	{/if}
</div>
