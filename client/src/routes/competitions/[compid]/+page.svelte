<script lang="ts">
import { page } from '$app/stores';
import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
import type { CompetitionResults } from '$lib/types';
import { BASE_URL, formatCompetitionDate } from '$lib/utils';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import { createQuery } from '@tanstack/svelte-query';

const compId = $page.params.compid;

const fetchResults = async () => {
	const response = await fetch(`${BASE_URL}/api/competitions/${compId}/results/`);
	return await response.json();
};

const query = createQuery<CompetitionResults>({
	queryKey: ['results', compId],
	queryFn: fetchResults
});
</script>

<Backbutton />
<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4">
		{#if $query.isError}
			<div class="rounded-lg bg-white p-12 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">Competition Not Found</h3>
				<p class="mt-2 text-gray-600">The requested competition could not be found.</p>
			</div>
		{:else if $query.isSuccess}
			<div class="mb-8">
				<h1 class="text-3xl font-bold text-gray-900">
					{$query.data.competition.name}
				</h1>
				<p class="mt-2 text-gray-600">
					Competition held on {formatCompetitionDate($query.data.competition.date)}
				</p>
			</div>
			<CompetitionResultsDisplay competitionResults={$query.data} />
		{:else}
			<LoadingScreen message="Loading Results" inline={true} minHeight="30rem" />
		{/if}
	</div>
</div>
