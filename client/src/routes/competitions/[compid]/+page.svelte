<script lang="ts">
import { onMount } from "svelte";
import { page } from "$app/stores";
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
					.map((event) => ({
						...event,
						rounds: event.rounds
							.map((round) => ({
								...round,
								results: round.results.filter((result) => studentStatus.includes(result.student_designator)),
							}))
							.filter((round) => round.results.length > 0),
					}))
					.filter((event) => event.rounds.length > 0),
			}
		: null;
});
</script>

<svelte:head>
	<title>
		{results?.competition.name ? `${results.competition.name} | Results` : "Competition Results"} | U of T Cube Club
	</title>
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		{#if loading}
			<div class="border border-border bg-surface p-12 text-center">
				<LoadingScreen message="Loading Results..." inline={true} minHeight="20rem" />
			</div>
		{:else if !hasError && filteredResults}
			<div class="mb-6">
				<div class="flex items-center gap-2">
					<a href="/competitions" class="text-xs font-semibold text-brand hover:underline">&larr; All Competitions</a>
					<span class="text-xs text-muted">•</span>
					{#if filteredResults.competition.session_name}
						<span class="rounded-sm bg-surface-muted px-2 py-0.5 text-xs font-semibold text-brand">
							{filteredResults.competition.session_name}
						</span>
					{/if}
					<span class="text-xs text-secondary">
						{formatCompetitionDate(filteredResults.competition.date)}
					</span>
				</div>
				<h1 class="mt-1 text-2xl font-bold tracking-tight text-main sm:text-3xl">
					{filteredResults.competition.name}
				</h1>
			</div>

			<!-- Filter Toolbar -->
			<div class="mb-6 flex flex-wrap items-center gap-3 border border-border bg-surface p-4 sm:p-5">
				<span class="text-xs font-semibold tracking-wider text-secondary uppercase">Status:</span>
				<UofTSelector bind:status={studentStatus} />
			</div>

			<CompetitionResultsDisplay competitionResults={filteredResults} />

			<div class="mt-8">
				<CompetitionScrambleTable results={results!.results} />
			</div>
		{:else}
			<div class="border border-border bg-surface p-12 text-center">
				<div class="mx-auto flex h-10 w-10 items-center justify-center rounded-sm bg-surface-muted text-secondary">
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="mt-3 text-base font-bold text-main">Competition Not Found</h3>
				<p class="mt-1 text-xs text-secondary">The requested competition could not be found or failed to load.</p>
			</div>
		{/if}
	</div>
</div>
