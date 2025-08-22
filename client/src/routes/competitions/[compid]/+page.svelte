<script lang="ts">
import { page } from '$app/stores';
import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
import type { CompetitionResults } from '$lib/types';
import { BASE_URL, fetchJson, formatCompetitionDate } from '$lib/utils';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import Switch from '$lib/components/Switch.svelte';

const compId = $page.params.compid;

let showUoftStudents = $state(false);
let loading = $state(true);
let error = $state(false);
let results: CompetitionResults | null = $state(null);

$effect(() => {
	fetchTimes(showUoftStudents);
});

const fetchTimes = async (showUoftOnly: boolean) => {
	loading = true;

	const url = new URL(`${BASE_URL}/api/competitions/${compId}/results/`);
	if (showUoftOnly) url.searchParams.append('uoft_only', '1');

	try {
		results = await fetchJson<CompetitionResults>(url);
	} catch (error) {
		console.error('Failed to fetch results:', error);
	} finally {
		loading = false;
	}
};
</script>

<svelte:head>
	<title>
		Results from {results?.competition.name ?? ""}
	</title>
</svelte:head>

<Backbutton />
<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4">
		{#if loading}
			<LoadingScreen message="Loading Results" inline={true} minHeight="30rem" />
		{:else if !error && results}
			<div class="mb-8 flex items-start justify-between">
				<div>
					<h1 class="text-3xl font-bold text-gray-900">
						{results.competition.name}
					</h1>
					<p class="mt-2 text-gray-600">
						{results.competition.session_name ? `${results.competition.session_name} Session - ` : ""}
						Date: {formatCompetitionDate(results.competition.date)}
					</p>
				</div>
				<div class="mt-2">
					<Switch label="Show UofT Students Only" bind:checked={showUoftStudents} />
				</div>
			</div>
			<CompetitionResultsDisplay competitionResults={results} />
		{:else}
			<div class="rounded-lg bg-white p-12 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">Competition Not Found</h3>
				<p class="mt-2 text-gray-600">The requested competition could not be found.</p>
			</div>
		{/if}
	</div>
</div>
