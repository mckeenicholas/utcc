<script lang="ts">
import { page } from '$app/stores';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import PersonalRecordsTable from '$lib/components/PersonalRecordsTable.svelte';
import CompetitionResultsTable from '$lib/components/CompetitionResultsTable.svelte';
import { type ProfileResponse, type WCAEvent } from '$lib/types';
import { BASE_URL, processPersonalRecords, generateRecordsForEvent, fetchJson } from '$lib/utils';
import { createQuery } from '@tanstack/svelte-query';

const personId = $page.params.id;
let selectedEvent: WCAEvent = $state('333');

const fetchProfileResults = async () => {
	const response = await fetchJson<ProfileResponse>(`${BASE_URL}/api/users/${personId}/results/`);

	const personalRecords = processPersonalRecords(response.records);
	const resultsTableContent = response.results.map(generateRecordsForEvent);

	return {
		records: personalRecords,
		results: resultsTableContent,
		name: response.person.name
	};
};

const query = createQuery({
	queryKey: ['personresults', personId],
	queryFn: fetchProfileResults
});
</script>

<svelte:head>
	<title>
		Results for {$query.data?.name ?? ""}
	</title>
</svelte:head>

<Backbutton />

{#if $query.isError}
	<div class="bg-gray-50 py-8">
		<div class="mx-auto max-w-6xl px-4">
			<div class="rounded-lg bg-white p-8 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">Person Not Found</h3>
				<p class="mt-2 text-gray-600">The requested person could not be found.</p>
			</div>
		</div>
	</div>
{:else if $query.isSuccess}
	<div class="bg-gray-50 py-8">
		<div class="mx-auto max-w-6xl px-4">
			<!-- Header -->
			<div class="mb-8">
				<h1 class="text-3xl font-bold text-gray-900">{$query.data.name}</h1>
				<p class="mt-2 text-gray-600">Competition Profile</p>
			</div>
			<!-- Personal Records -->
			<PersonalRecordsTable records={$query.data.records} />
			<!-- Competition Results -->
			<CompetitionResultsTable results={$query.data.results} selectedEvent={selectedEvent} />
		</div>
	</div>
{:else}
	<LoadingScreen message="Loading Profile" inline={true} minHeight="30rem" />
{/if}
