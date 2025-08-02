<script lang="ts">
	import type { CompetitionResults } from '$lib/types';
	import { BASE_URL } from '$lib/utils';
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';

	let competitionResults: CompetitionResults | null = $state(null);
	let loading = $state(false);
	let compId = page.params.compid;

	const fetchCompetitionResults = async () => {
		const competitionResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/results/`);
		competitionResults = await competitionResponse.json();
	};

	onMount(fetchCompetitionResults);
</script>

{#if loading}
	<p>Loading</p>
{:else if competitionResults}
	<CompetitionResultsDisplay {competitionResults} />
{/if}
