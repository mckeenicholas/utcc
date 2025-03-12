<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
	import type { CompetitionResults } from '$lib/types';
	import { resultsURL } from '$lib/utils';

	let competitionResults = $state<CompetitionResults | null>(null);

	onMount(async () => {
		const compid = parseInt($page.params.compid);
		const url = `${resultsURL}${compid}/`;

		const response = await fetch(url);
		const data: CompetitionResults = await response.json();

		competitionResults = data;
	});
</script>

{#if competitionResults}
	<CompetitionResultsDisplay {competitionResults} />
{/if}
