<script lang="ts">
import { onMount } from "svelte";
import { page } from "$app/stores";
import Backbutton from "$lib/components/Backbutton.svelte";
import CompetitionResultsDisplay from "$lib/components/CompetitionResultsDisplay.svelte";
import CompetitionScrambleTable from "$lib/components/CompetitionScrambleTable.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import UofTSelector from "$lib/components/UofTSelector.svelte";
import type { CompetitionResults, StudentStatus } from "$lib/types";
import { BASE_URL, fetchJson, formatCompetitionDate } from "$lib/utils";

const compId = $page.params.compid;

let studentStatus: StudentStatus = $state([]);
let loading = $state(true);
let hasError = $state(false);
let results: CompetitionResults | null = $state(null);

const fetchTimes = async () => {
	loading = true;

	const url = new URL(`${BASE_URL}/api/competitions/${compId}/results/`);

	try {
		results = await fetchJson<CompetitionResults>(url);
	} catch (error) {
		console.error("Failed to fetch results:", error);
		hasError = true;
	} finally {
		loading = false;
	}
};

onMount(fetchTimes);

const filteredResults: CompetitionResults | null = $derived.by(() => {
	if (studentStatus.length === 0) {
		return results;
	}

	return results
		? {
				...results,
				results: results.results
					.map((event) =>
						Object.assign({}, event, {
							rounds: event.rounds
								.map((round) => ({
									...round,
									results: round.results.filter((result) => studentStatus.includes(result.student_designator)),
								}))
								.filter((round) => round.results.length > 0),
						}),
					)
					.filter((event) => event.rounds.length > 0),
			}
		: null;
});
</script>

<svelte:head>
	<title>
		Results from {results?.competition.name ?? "competition"}
	</title>
</svelte:head>

<Backbutton />
<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4">
		{#if loading}
			<LoadingScreen message="Loading Results" inline={true} minHeight="30rem" />
		{:else if !hasError && filteredResults}
			<div class="mb-8 flex items-start justify-between">
				<div>
					<h1 class="text-3xl font-bold text-gray-900">
						{filteredResults.competition.name}
					</h1>
					<p class="mt-2 text-gray-600">
						{filteredResults.competition.session_name ? `${filteredResults.competition.session_name} Session - ` : ""}
						Date: {formatCompetitionDate(filteredResults.competition.date)}
					</p>
				</div>
				<div class="mt-2">
					<UofTSelector bind:status={studentStatus} />
				</div>
			</div>
			<CompetitionResultsDisplay competitionResults={filteredResults} />
			<div class="mt-8">
				<CompetitionScrambleTable results={results!.results} />
			</div>
		{:else}
			<div class="rounded-lg bg-white p-12 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">Competition Not Found</h3>
				<p class="mt-2 text-gray-600">The requested competition could not be found.</p>
			</div>
		{/if}
	</div>
</div>
