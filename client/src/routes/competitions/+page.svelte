<script lang="ts">
import { onMount } from "svelte";
import CompetitionCard from "$lib/components/CompetitionCard.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PaginationControls from "$lib/components/PaginationControls.svelte";
import SelectMenu from "$lib/components/SelectMenu.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import UofTSelector from "$lib/components/UofTSelector.svelte";
import { fetchSessions } from "$lib/competitionSessionService";
import type { Competition, Paginated, Session, StudentStatus } from "$lib/types";
import { BASE_URL, PAGINATION_SIZE, fetchJson, toInt } from "$lib/utils";

let competitions: Competition[] = $state([]);
let loading = $state(true);
let errorMessage = $state<string | null>(null);
let currentPage = $state(1);
let totalPages = $state(1);
let hasNext = $state(false);
let hasPrevious = $state(false);
let totalCount = $state(0);
let allSessions: Session[] = $state([]);
let selectedSession: string = $state("-1");
let selectedDesignator: StudentStatus = $state([]);
let selectedOrdering: string = $state("-date");

const sortOptions = [
	{ label: "Date: Newest First", value: "-date" },
	{ label: "Date: Oldest First", value: "date" },
	{ label: "Name: A to Z", value: "name" },
	{ label: "Name: Z to A", value: "-name" },
	{ label: "Designator: A to Z", value: "student_designator" },
	{ label: "Designator: Z to A", value: "-student_designator" },
];

const selectedOrderingLabel = $derived(
	sortOptions.find((o) => o.value === selectedOrdering)?.label ?? "Date: Newest First",
);

$effect(() => {
	// Reset to page 1 whenever any filters change
	const _ = [selectedSession, selectedDesignator, selectedOrdering];
	currentPage = 1;
});

$effect(() => {
	fetchCompetitions(currentPage, toInt(selectedSession) ?? -1, selectedDesignator, selectedOrdering);
});

const fetchCompetitions = async (page = 1, sessionId = -1, designator: string[] = [], ordering = "-date") => {
	loading = true;
	errorMessage = null;

	try {
		const url = new URL(`${BASE_URL}/api/competitions/`);
		url.searchParams.set("page", page.toString());
		if (sessionId !== -1) {
			url.searchParams.set("session_id", sessionId.toString());
		}
		if (designator.length > 0) {
			designator.forEach((d) => {
				url.searchParams.append("student_designator", d);
			});
		}
		if (ordering) {
			url.searchParams.set("ordering", ordering);
		}

		const data = await fetchJson<Paginated<Competition>>(url);

		competitions = data.results;
		currentPage = page;
		totalCount = data.count;
		hasNext = Boolean(data.next);
		hasPrevious = Boolean(data.previous);
		totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
	} catch (error) {
		console.error("Error fetching competitions:", error);
		errorMessage = "Failed to load competitions. Please try again later.";
	} finally {
		loading = false;
	}
};

onMount(async () => {
	allSessions = await fetchSessions();
});

const goToNextPage = () => {
	if (hasNext) {
		fetchCompetitions(currentPage + 1, toInt(selectedSession) ?? -1, selectedDesignator, selectedOrdering);
	}
};

const goToPreviousPage = () => {
	if (hasPrevious) {
		fetchCompetitions(currentPage - 1, toInt(selectedSession) ?? -1, selectedDesignator, selectedOrdering);
	}
};

const goToPage = (page: number) => {
	if (page >= 1 && page <= totalPages) {
		fetchCompetitions(page, toInt(selectedSession) ?? -1, selectedDesignator, selectedOrdering);
	}
};
</script>

<svelte:head>
	<title>Competitions | University of Toronto Cube Club</title>
	<meta name="description" content="University of Toronto Rubik's Cube Club competitions archive." />
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<div class="mb-6">
			<h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Competitions</h1>
			<p class="mt-1 text-sm text-gray-700">Browse official club tournaments and sessions.</p>
		</div>

		<!-- Filter Bar -->
		<div class="mb-6 flex flex-wrap items-center gap-4 border border-gray-200 bg-white p-4 sm:p-5">
			<div class="flex items-center gap-2">
				<span class="text-xs font-medium text-gray-700">Session:</span>
				<SessionSelector bind:value={selectedSession} sessionData={allSessions} />
			</div>
			<div class="flex items-center gap-2">
				<span class="text-xs font-medium text-gray-700">Status:</span>
				<UofTSelector bind:status={selectedDesignator} />
			</div>
			<div class="flex items-center gap-2">
				<span class="text-xs font-medium text-gray-700">Order:</span>
				<div class="w-44">
					<SelectMenu bind:value={selectedOrdering} options={sortOptions} />
				</div>
			</div>
		</div>

		{#if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen message="Loading Competitions..." inline />
			</div>
		{:else if errorMessage}
			<div class="border border-red-200 bg-white p-8 text-center sm:p-12">
				<div class="mx-auto flex h-10 w-10 items-center justify-center rounded bg-red-50 text-uoft-warm-red">
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="mt-3 text-base font-bold text-gray-900">Error Loading Competitions</h3>
				<p class="mt-1 text-sm text-gray-600">{errorMessage}</p>
				<button
					onclick={() => window.location.reload()}
					class="mt-4 inline-flex items-center rounded-sm bg-uoft-blue px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-uoft-blue-80 focus:outline-none"
				>
					Try Again
				</button>
			</div>
		{:else if competitions.length > 0}
			<!-- Competitions List -->
			<div class="space-y-3">
				{#each competitions as competition (competition.id)}
					<CompetitionCard {competition} />
				{/each}
			</div>

			{#if totalPages > 1}
				<div class="mt-4 border border-gray-200 bg-white p-4">
					<PaginationControls
						{currentPage}
						{totalPages}
						{totalCount}
						itemsPerPage={PAGINATION_SIZE}
						{hasNext}
						{hasPrevious}
						onPageChange={goToPage}
						onNext={goToNextPage}
						onPrevious={goToPreviousPage}
					/>
				</div>
			{/if}
		{:else}
			<!-- Empty State -->
			<div class="border border-gray-200 bg-white p-12 text-center">
				<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-sm bg-gray-100 text-gray-700">
					<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
						/>
					</svg>
				</div>
				<h3 class="mt-3 text-base font-bold text-gray-900">No Competitions Found</h3>
				<p class="mt-1 text-xs text-gray-700">There are no competitions matching the selected filters.</p>
			</div>
		{/if}
	</div>
</div>
