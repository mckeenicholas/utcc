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
			const compid = parseInt($page.params.compid);
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

<Backbutton to="/results" />

{#if loading}
	<LoadingScreen message="Loading Results" />
{:else if competitionResults}
	<div class="min-h-screen bg-gray-50 py-8">
		<div class="mx-auto max-w-6xl px-4">
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
		</div>
	</div>
{:else}
	<div class="min-h-screen bg-gray-50 py-8">
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
				<h3 class="mt-4 text-lg font-medium text-gray-900">Competition Not Found</h3>
				<p class="mt-2 text-gray-600">The requested competition could not be found.</p>
			</div>
		</div>
	</div>
{/if}
