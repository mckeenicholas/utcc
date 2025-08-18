<script lang="ts">
import { type Competition, type CompetitionResults, type Paginated } from '$lib/types';
import CompetitionResultsDisplay from '$lib/components/CompetitionResultsDisplay.svelte';
import {
	fetchJson,
	formatCompetitionDate,
	latestCompetitionsURL,
	latestResultsURL
} from '$lib/utils';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import { createQuery } from '@tanstack/svelte-query';

const queryResults = async () => await fetchJson<CompetitionResults>(latestResultsURL);
const queryCompetitions = async () =>
	(await fetchJson<Paginated<Competition>>(latestCompetitionsURL)).results.slice(0, 10);

const competitionsQuery = createQuery({
	queryKey: ['home-competiitons'],
	queryFn: queryCompetitions
});
const resultsQuery = createQuery({ queryKey: ['home-results'], queryFn: queryResults });
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-6xl px-4">
		<!-- Header -->
		<div class="ms-2 mb-6">
			<h1 class="text-3xl font-bold text-gray-900">UofT Rubik's Cube Club</h1>
			<p class="mt-2 text-gray-600">Club Meeting Results</p>
		</div>

		<!-- Navigation Section -->
		{#if $competitionsQuery.isSuccess}
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
						{#each $competitionsQuery.data as competition (competition.id)}
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
		{#if $resultsQuery.isSuccess}
			{@const competition = $resultsQuery.data.competition}
			<div class="rounded-lg bg-white shadow-sm">
				<div class="border-b border-gray-200 px-6 py-4">
					<h2 class="text-xl font-semibold text-gray-800">
						<a href="/competitions/{competition.id}">
							Most Recent Results: {competition.name}
						</a>
					</h2>
					<p class="mt-1 text-sm text-gray-600">
						Latest competition results from {formatCompetitionDate(competition.date)}
					</p>
				</div>
				<div class="p-6">
					<CompetitionResultsDisplay competitionResults={$resultsQuery.data} />
				</div>
			</div>
		{:else}
			<LoadingScreen inline message="Loading Results" />
		{/if}
	</div>
</div>
