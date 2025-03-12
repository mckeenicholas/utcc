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

<div class="m-4 mb-3">
	<a class="rounded-md bg-gray-200 p-2 text-xl hover:bg-gray-300" href="/results"> ← Back </a>
</div>
{#if competitionResults}
	<CompetitionResultsDisplay {competitionResults} />
{/if}
