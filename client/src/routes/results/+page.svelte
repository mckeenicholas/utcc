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

	function handleCompetitionSelect(event: Event) {
		const select = event.target as HTMLSelectElement;
		const id = parseInt(select.value);
		if (id) {
			window.location.href = `/results/${id}`;
		}
	}
</script>

{#if competitionsList}
	<div class="m-4 w-64">
		<label for="competition-select" class="mb-1 block text-sm font-medium text-gray-700">
			View past results
		</label>
		<select
			id="competition-select"
			class="block w-full rounded-md bg-gray-200 shadow-sm focus:border-blue-500 focus:ring-blue-500"
			onchange={handleCompetitionSelect}
		>
			{#each competitionsList.competitions as competition}
				<option value={competition.id}>
					{competition.name} ({competition.date})
				</option>
			{/each}
		</select>
	</div>
{/if}

{#if competitionResults}
	<CompetitionResultsDisplay {competitionResults} />
{/if}
