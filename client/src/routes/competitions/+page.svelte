<script lang="ts">
import { onMount } from "svelte";
import Backbutton from "$lib/components/Backbutton.svelte";
import CompetitionCard from "$lib/components/CompetitionCard.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PaginationControls from "$lib/components/PaginationControls.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import UofTSelector from "$lib/components/UofTSelector.svelte";
import { Select } from "bits-ui";
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
	<title>UofT Rubik's Cube Club Competition Search</title>
	<meta name="description" content="University of Toronto Rubik's Cube Club competition search." />
</svelte:head>

<Backbutton />
<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-6xl px-4">
		<div class="mb-6">
			<h1 class="text-3xl font-bold text-gray-900">All Competitions</h1>
			<p class="mt-2 text-gray-600">Browse club-sanctioned competitions</p>
		</div>

		<!-- Filter Bar -->
		<div
			class="mb-8 flex flex-col gap-4 rounded-lg border border-gray-200 bg-white p-4 shadow-sm md:flex-row md:items-center md:justify-between"
		>
			<div class="flex flex-col gap-1.5 sm:flex-row sm:items-center">
				<span class="text-sm font-medium text-gray-700">Academic Session:</span>
				<SessionSelector bind:value={selectedSession} sessionData={allSessions} class="shadow-sm" />
			</div>
			<div class="flex flex-col gap-1.5 sm:flex-row sm:items-center">
				<span class="text-sm font-medium text-gray-700">Designation:</span>
				<UofTSelector bind:status={selectedDesignator} />
			</div>
			<div class="flex flex-col gap-1.5 sm:flex-row sm:items-center">
				<span class="text-sm font-medium text-gray-700">Sort by:</span>
				<div class="w-full sm:w-48">
					<Select.Root items={sortOptions} bind:value={selectedOrdering} type="single">
						<Select.Trigger
							class="flex h-[38px] w-full cursor-pointer items-center justify-between rounded-md border border-gray-200 bg-white px-3 py-2 text-left text-sm text-gray-700 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
							aria-label="Select sorting order"
						>
							<span>{selectedOrderingLabel}</span>
							<svg class="ml-2 h-4 w-4 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
							</svg>
						</Select.Trigger>
						<Select.Portal>
							<Select.Content
								class="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 z-50 max-h-96 w-[var(--bits-select-anchor-width)] min-w-[var(--bits-select-anchor-width)] overflow-hidden rounded-md border border-gray-200 bg-white py-1 shadow-lg"
								sideOffset={4}
							>
								<Select.Viewport class="p-1">
									{#each sortOptions as option (option.value)}
										<Select.Item
											class="relative flex w-full cursor-default items-center rounded-sm py-1.5 pr-2 pl-8 text-sm outline-none select-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:pointer-events-none data-[disabled]:opacity-50 data-[highlighted]:bg-gray-100"
											value={option.value}
											label={option.label}
										>
											{#snippet children({ selected })}
												{#if selected}
													<span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
														<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
															<path
																stroke-linecap="round"
																stroke-linejoin="round"
																stroke-width="2"
																d="M5 13l4 4L19 7"
															/>
														</svg>
													</span>
												{/if}
												{option.label}
											{/snippet}
										</Select.Item>
									{/each}
								</Select.Viewport>
							</Select.Content>
						</Select.Portal>
					</Select.Root>
				</div>
			</div>
		</div>

		{#if loading}
			<LoadingScreen message="Loading Competitions" />
		{:else if errorMessage}
			<div class="rounded-lg bg-red-50 p-6 text-center shadow-sm">
				<div class="mx-auto h-12 w-12 text-red-400">
					<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
						/>
					</svg>
				</div>
				<h3 class="mt-4 text-lg font-medium text-red-900">Error Loading Competitions</h3>
				<p class="mt-2 text-red-700">{errorMessage}</p>
				<button
					onclick={() => window.location.reload()}
					class="mt-4 inline-flex items-center rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:ring-2 focus:ring-red-500 focus:ring-offset-2 focus:outline-none"
				>
					Try Again
				</button>
			</div>
		{:else if competitions.length > 0}
			<!-- Competitions List -->
			<div class="space-y-4">
				{#each competitions as competition (competition.id)}
					<CompetitionCard {competition} />
				{/each}
			</div>

			{#if totalPages > 1}
				<div class="mt-4 rounded-md bg-white p-4 shadow">
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
			<div class="rounded-lg bg-white p-12 text-center shadow-sm">
				<div class="mx-auto h-12 w-12 text-gray-400">
					<svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
						/>
					</svg>
				</div>
				<h3 class="mt-4 text-lg font-medium text-gray-900">No Competitions Found</h3>
				<p class="mt-2 text-gray-600">There are no competitions matching the selected filters.</p>
			</div>
		{/if}
	</div>
</div>
