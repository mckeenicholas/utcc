<script lang="ts">
	import { onMount } from 'svelte';
	import { type CompetitionList, type CompetitionResults } from '$lib/types';
	import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
	import { resultsURL, competitionsURL } from '$lib/utils';

	let competitionResults = $state<CompetitionResults | null>(null);
	let competitionsList = $state<CompetitionList | null>(null);

	onMount(async () => {
		const [resultsData, competitionsData] = await Promise.all([
			fetch(resultsURL).then((res) => res.json()),
			fetch(competitionsURL).then((res) => res.json())
		]);

		console.log(resultsData);

		competitionResults = resultsData;
		competitionsList = competitionsData;
	});
</script>

<div class="flex justify-center">
	{#if competitionsList}
		<div class="m-4 flex w-full items-center rounded-md bg-gray-200 shadow-sm">
			<p class="ms-2 block whitespace-nowrap font-medium">Past competitions:</p>
			<div class="max-w-full overflow-x-auto whitespace-nowrap">
				{#each competitionsList.competitions as competition (competition.id)}
					<a href={`/results/${competition.id}`} class="inline-block p-2 hover:bg-gray-300">
						{competition.name}
					</a>
				{/each}
			</div>
		</div>
	{/if}
</div>

{#if competitionResults}
	<hr />
	<CompetitionResultsDisplay
		{competitionResults}
		title={`Most recent results: ${competitionResults.competition.name}`}
	/>
{/if}
