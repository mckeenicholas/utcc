<script lang="ts">
import { onMount } from 'svelte';
import { type Competition, type CompetitionResults, type Paginated } from '$lib/types';
import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
import { latestCompetitionsURL, latestResultsURL } from '$lib/utils';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';

let competitionResults = $state<CompetitionResults | null>(null);
let competitionsList = $state<Competition[] | null>(null);
let loading = $state(true);

onMount(async () => {
	try {
		const [resultsData, competitionsData]: [CompetitionResults, Paginated<Competition>] =
			await Promise.all([
				fetch(latestResultsURL).then((res) => res.json()),
				fetch(latestCompetitionsURL).then((res) => res.json())
			]);

		competitionResults = resultsData;
		// Only show the last 10 competitions
		competitionsList = competitionsData.results.slice(0, 10);
	} catch (error) {
		console.error('Failed to fetch data:', error);
	} finally {
		loading = false;
	}
});
</script>

{#if loading}
	<LoadingScreen message="Loading Results" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-6xl px-4">
			<!-- Header -->
			<div class="ms-2 mb-6">
				<h1 class="text-3xl font-bold text-gray-900">UofT Rubik's Cube Club</h1>
				<p class="mt-2 text-gray-600">Club Meeting Results</p>
			</div>

			<!-- Navigation Section -->
			{#if competitionsList}
				<div class="mb-8 rounded-lg bg-white p-4 shadow-sm">
					<div class="flex flex-wrap items-center gap-2">
						<a
							href="/records"
							class="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
						>
							<svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z"
								/>
							</svg>
							Records
						</a>
						<a
							href="/competitions"
							class="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
						>
							<svg
								class="mr-2 h-4 w-4"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<path d="M8 2v4" />
								<path d="M16 2v4" />
								<rect width="18" height="18" x="3" y="4" rx="2" />
								<path d="M3 10h18" />
							</svg>
							All Competitions
						</a>
						<a
							href="/rankings"
							class="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
						>
							<svg
								class="mr-2 h-4 w-4"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<path d="M3 12h.01" />
								<path d="M3 18h.01" />
								<path d="M3 6h.01" />
								<path d="M8 12h13" />
								<path d="M8 18h13" />
								<path d="M8 6h13" />
							</svg>
							Rankings
						</a>
						<a
							href="/persons"
							class="inline-flex items-center rounded-md bg-blue-600 px-3 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none"
						>
							<svg
								class="mr-2 h-4 w-4"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
								stroke-width="2"
								stroke-linecap="round"
								stroke-linejoin="round"
							>
								<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
								<circle cx="12" cy="7" r="4" />
							</svg>
							Persons
						</a>
						<div class="flex flex-wrap items-center gap-2">
							<span class="text-sm font-medium text-gray-700">Recent competitions:</span>
							{#each competitionsList as competition (competition.id)}
								<a
									href="/competitions/{competition.id}"
									class="inline-block rounded-md bg-gray-200 px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-300 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
								>
									{competition.name}
								</a>
							{/each}
						</div>
					</div>
				</div>
			{/if}

			<!-- Recent Results Section -->
			{#if competitionResults}
				<div class="rounded-lg bg-white shadow-sm">
					<div class="border-b border-gray-200 px-6 py-4">
						<h2 class="text-xl font-semibold text-gray-800">
							<a href="/competitions/{competitionResults.competition.id}">
								Most Recent Results: {competitionResults.competition.name}
							</a>
						</h2>
						<p class="mt-1 text-sm text-gray-600">
							Latest competition results from {new Date(
								competitionResults.competition.date
							).toLocaleDateString()}
						</p>
					</div>
					<div class="p-6">
						<CompetitionResultsDisplay competitionResults={competitionResults} />
					</div>
				</div>
			{:else}
				<div class="rounded-lg bg-white p-6 text-center shadow-sm">
					<div class="mx-auto h-12 w-12 text-gray-400">
						<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
							/>
						</svg>
					</div>
					<h3 class="mt-4 text-lg font-medium text-gray-900">No Results Available</h3>
					<p class="mt-2 text-gray-600">
						There are no competition results to display at this time.
					</p>
				</div>
			{/if}
		</div>
	</div>
{/if}
