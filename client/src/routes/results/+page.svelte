<script lang="ts">
import { onMount } from "svelte";
import CompetitionResultsDisplay from "$lib/components/CompetitionResultsDisplay.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import { type Competition, type CompetitionResults, type Paginated } from "$lib/types";
import { fetchJson, formatCompetitionDate, latestCompetitionsURL, latestResultsURL } from "$lib/utils";

let latestResults: CompetitionResults | null = $state(null);
let competitionList: Competition[] | null = $state(null);

const queryResults = async () => await fetchJson<CompetitionResults>(latestResultsURL);
const queryCompetitions = async () => {
	const data = await fetchJson<Paginated<Competition>>(latestCompetitionsURL);
	return data.results.slice(0, 8);
};

const fetchPageData = async () => {
	try {
		const [resultsData, competitions] = await Promise.all([queryResults(), queryCompetitions()]);

		latestResults = resultsData;
		competitionList = competitions;
	} catch (error) {
		console.error("Error loading main page results", error);
	}
};

onMount(fetchPageData);
</script>

<svelte:head>
	<title>UofT Rubik's Cube Club Results</title>
	<meta
		name="description"
		content="Recent results and competitions held by the University of Toronto Rubik's Cube Club."
	/>
</svelte:head>

<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8">
		<!-- Header -->
		<div class="mb-8">
			<h1 class="text-3xl font-extrabold tracking-tight text-gray-900">Club Meeting Results</h1>
			<p class="mt-2 text-base text-gray-600">Browse the latest results and past meeting files.</p>
		</div>

		<!-- Recent Competitions Bar -->
		{#if competitionList}
			<div class="mb-8 rounded-xl border border-gray-200 bg-white p-5 shadow-sm">
				<div class="flex flex-col gap-3 sm:flex-row sm:items-center">
					<span class="shrink-0 text-sm font-bold text-gray-700">Recent Competitions:</span>
					<div class="flex flex-wrap gap-2">
						{#each competitionList as competition (competition.id)}
							<a
								href="/competitions/{competition.id}"
								class="inline-flex items-center rounded-lg border border-gray-200 bg-gray-50 px-3 py-1 text-xs font-semibold text-gray-700 transition-all hover:border-gray-300 hover:bg-gray-100 hover:text-gray-900 focus:outline-none"
							>
								{competition.name}
							</a>
						{/each}
					</div>
				</div>
			</div>
		{/if}

		<!-- Recent Results Section -->
		{#if latestResults}
			{@const competition = latestResults.competition}
			<div class="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm">
				<div class="border-b border-gray-100 bg-gray-50/50 px-6 py-5">
					<h2 class="text-xl font-bold text-gray-900">
						<a href="/competitions/{competition.id}" class="transition-colors hover:text-blue-600">
							Most Recent Results: {competition.name}
						</a>
					</h2>
					<p class="mt-1.5 text-sm font-medium text-gray-500">
						Latest competition results from {formatCompetitionDate(competition.date)}
					</p>
				</div>
				<div class="p-6">
					<CompetitionResultsDisplay competitionResults={latestResults} />
				</div>
			</div>
		{:else}
			<div class="flex min-h-[300px] items-center justify-center">
				<LoadingScreen inline message="Loading Results" />
			</div>
		{/if}
	</div>
</div>
