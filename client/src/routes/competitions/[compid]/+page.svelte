<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
	import type { CompetitionResults } from '$lib/types';
	import { BASE_URL } from '$lib/utils';
	import Backbutton from '$lib/components/Backbutton.svelte';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';

	let competitionResults = $state<CompetitionResults | null>(null);
	let loading = $state(true);

	onMount(async () => {
		try {
			const compid = parseInt($page.params.compid ?? '0');
			const url = `${BASE_URL}/api/competitions/${compid}/results/`;

			const response = await fetch(url);
			const data: CompetitionResults = await response.json();

			competitionResults = data;
		} catch (error) {
			console.error('Failed to fetch competition results:', error);
		} finally {
			loading = false;
		}
	});
</script>

<Backbutton />

<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4">
		{#if loading}
			<LoadingScreen message="Loading Results" inline={true} minHeight="30rem" />
		{:else if competitionResults}
			<!-- Header -->
			<div class="mb-8">
				<h1 class="text-3xl font-bold text-gray-900">
					{competitionResults.competition.name}
				</h1>
				<p class="mt-2 text-gray-600">
					Competition held on {new Date(competitionResults.competition.date).toLocaleDateString()}
				</p>
			</div>

			<!-- Results Display -->
			<CompetitionResultsDisplay {competitionResults} />
		{:else}
			<div class="rounded-lg bg-white p-12 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">Competition Not Found</h3>
				<p class="mt-2 text-gray-600">The requested competition could not be found.</p>
			</div>
		{/if}
	</div>
</div>
