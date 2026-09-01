<script lang="ts">
import { onMount } from "svelte";
import CompetitionResultsDisplay from "$lib/components/CompetitionResultsDisplay.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import SelectMenu from "$lib/components/SelectMenu.svelte";
import UofTSelector from "$lib/components/UofTSelector.svelte";
import {
	type Competition,
	type CompetitionResults,
	type Paginated,
	type StudentStatus,
	type WCAEvent,
	eventNames,
} from "$lib/types";
import {
	BASE_URL,
	fetchJson,
	formatCompetitionDate,
	latestCompetitionsURL,
	latestResultsURL,
	sortEvents,
} from "$lib/utils";

let results: CompetitionResults | null = $state(null);
let competitionList = $state<Competition[] | null>(null);
let selectedCompetitionId = $state<number | null>(null);
let selectedCompValue = $state<string>("");
let studentStatus = $state<StudentStatus>([]);
let loading = $state(true);
let hasError = $state(false);

const competitionOptions = $derived(
	competitionList?.map((comp) => ({
		label: `${comp.name} (${formatCompetitionDate(comp.date)})`,
		value: comp.id.toString(),
	})) ?? [],
);

$effect(() => {
	if (selectedCompetitionId !== null) {
		selectedCompValue = selectedCompetitionId.toString();
	}
});

$effect(() => {
	if (selectedCompValue && Number(selectedCompValue) !== selectedCompetitionId) {
		switchCompetition(Number(selectedCompValue));
	}
});

const fetchLatest = async () => {
	loading = true;
	hasError = false;
	try {
		const [resultsData, competitionsData] = await Promise.all([
			fetchJson<CompetitionResults>(latestResultsURL),
			fetchJson<Paginated<Competition>>(latestCompetitionsURL),
		]);

		results = resultsData;
		competitionList = competitionsData.results.slice(0, 10);
		if (resultsData?.competition) {
			selectedCompetitionId = resultsData.competition.id;
		}
	} catch (error) {
		console.error("Error loading results:", error);
		hasError = true;
	} finally {
		loading = false;
	}
};

const switchCompetition = async (compId: number) => {
	if (selectedCompetitionId === compId) {
		return;
	}
	selectedCompetitionId = compId;
	loading = true;
	hasError = false;
	try {
		const compResults = await fetchJson<CompetitionResults>(`${BASE_URL}/api/competitions/${compId}/results/`);
		results = compResults;
	} catch (error) {
		console.error("Failed to fetch competition results:", error);
		hasError = true;
	} finally {
		loading = false;
	}
};

onMount(fetchLatest);

const filteredResults: CompetitionResults | null = $derived.by(() => {
	if (!results) {
		return null;
	}
	if (studentStatus.length === 0) {
		return results;
	}

	return {
		...results,
		results: results.results
			.map((event) => ({
				...event,
				rounds: event.rounds
					.map((round) => ({
						...round,
						results: round.results.filter((res) => studentStatus.includes(res.student_designator)),
					}))
					.filter((round) => round.results.length > 0),
			}))
			.filter((event) => event.rounds.length > 0),
	};
});

const availableEvents: WCAEvent[] = $derived.by(() => {
	if (!results?.results) {
		return [];
	}
	return results.results.map((r) => r.event).toSorted(sortEvents);
});

const scrollToEvent = (eventId: string) => {
	const element = document.querySelector(`#event-${eventId}`);
	if (element) {
		element.scrollIntoView({ behavior: "smooth", block: "start" });
	}
};
</script>

<svelte:head>
	<title>Results | University of Toronto Cube Club</title>
	<meta
		name="description"
		content="Official competition results, solve times, and round standings for the University of Toronto Rubik's Cube Club."
	/>
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<!-- Header -->
		<div class="mb-6">
			{#if results?.competition}
				{@const comp = results.competition}
				<div class="flex items-center gap-2">
					{#if comp.session_name}
						<span class="rounded-sm bg-gray-100 px-2 py-0.5 text-xs font-semibold text-uoft-blue">
							{comp.session_name}
						</span>
					{/if}
					<span class="text-xs text-gray-700">
						{formatCompetitionDate(comp.date)}
					</span>
				</div>
				<h1 class="mt-1 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
					{comp.name}
				</h1>
			{:else if loading}
				<div class="h-8 w-64 animate-pulse bg-gray-200"></div>
			{/if}
		</div>

		<!-- Toolbar: Switcher & Status Filter -->
		<div class="mb-6 flex flex-wrap items-center gap-4 border border-gray-200 bg-white p-4 sm:p-5">
			{#if competitionList && competitionList.length > 0}
				<div class="flex items-center gap-2">
					<span class="text-xs font-medium text-gray-700">Competition:</span>
					<div class="w-56 sm:w-64">
						<SelectMenu
							bind:value={selectedCompValue}
							options={competitionOptions}
							placeholder="Select competition..."
						/>
					</div>
				</div>
			{/if}

			<div class="flex items-center gap-2">
				<span class="text-xs font-medium text-gray-700">Status:</span>
				<UofTSelector bind:status={studentStatus} />
			</div>
		</div>

		<!-- Sticky Event Navigation Strip -->
		{#if availableEvents.length > 0}
			<div
				class="sticky top-0 z-20 -mx-4 mb-6 overflow-x-auto border-y border-gray-200 bg-white px-4 py-2.5 sm:mx-0 sm:border"
			>
				<div class="flex items-center gap-1.5">
					<span class="mr-2 shrink-0 text-xs font-bold tracking-wider text-uoft-blue uppercase"> Jump to: </span>
					{#each availableEvents as event (event)}
						<button
							type="button"
							class="inline-flex cursor-pointer items-center gap-1.5 rounded-sm bg-gray-100 px-2.5 py-1 text-xs font-medium text-gray-700 transition-colors hover:bg-uoft-blue hover:text-white"
							onclick={() => scrollToEvent(event)}
						>
							<span class="cubing-icon event-{event} text-sm"></span>
							<span class="whitespace-nowrap">{eventNames[event]}</span>
						</button>
					{/each}
				</div>
			</div>
		{/if}

		<!-- Main Results Section -->
		{#if loading && !results}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen inline message="Loading Competition Results..." />
			</div>
		{:else if hasError}
			<div class="border border-red-200 bg-white p-8 text-center sm:p-12">
				<div class="mx-auto flex h-10 w-10 items-center justify-center rounded bg-red-50 text-uoft-warm-red">
					<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
						/>
					</svg>
				</div>
				<h3 class="mt-3 text-base font-bold text-gray-900">Failed to Load Results</h3>
				<p class="mt-1 text-sm text-gray-600">Could not retrieve competition results from the server.</p>
				<button
					type="button"
					class="mt-4 inline-flex items-center rounded-sm bg-uoft-blue px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-uoft-blue-80 focus:outline-none"
					onclick={fetchLatest}
				>
					Retry
				</button>
			</div>
		{:else if filteredResults}
			<CompetitionResultsDisplay competitionResults={filteredResults} />
		{/if}
	</div>
</div>
