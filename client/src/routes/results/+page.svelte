<script lang="ts">
	import { onMount } from 'svelte';
	import { eventNames, type CompetitionResults } from '../../lib/types';

	const url = 'http://localhost:8000/results';

	let competitionResults = $state<CompetitionResults | null>(null);

	onMount(async () => {
		const response = await fetch(url);
		const data: CompetitionResults = await response.json();

		competitionResults = data;
	});
</script>

{#if competitionResults}
	<h1>Results for {competitionResults.competition.name}</h1>
	<ul>
		{#each Object.entries(competitionResults.results) as [eventId, results]}
			<li>
				{eventNames[eventId as keyof typeof eventNames]}
			</li>
		{/each}
	</ul>
{/if}
