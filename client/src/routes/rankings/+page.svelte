<script lang="ts">
import { SvelteURLSearchParams } from "svelte/reactivity";
import LoadingScreen from "#lib/components/LoadingScreen.svelte";
import PaginationControls from "#lib/components/PaginationControls.svelte";
import RankingSelector from "#lib/components/RankingSelector.svelte";
import {
	type Paginated,
	type RecordInstance,
	type StudentStatus,
	type WCAEvent,
	eventNames,
	eventSolves,
} from "#lib/types.js";
import { BASE_URL, PAGINATION_SIZE, fetchJson, isSinglePrimaryEvent, renderTime } from "#lib/utils.js";

let selectedEvent: WCAEvent = $state("333");
let previousEvent: WCAEvent = $state("333");
let isAverage = $state(false);
let showAllResults = $state(false);
let pageNum = $state(1);
let selectedSession: string = $state("-1");
let uoftStudentStatus: StudentStatus = $state([]);
let results: Paginated<RecordInstance> | null = $state(null);
let loading = $state(true);
let currentPage = $state(1);
let totalPages = $state(1);
let hasNext = $state(false);
let hasPrevious = $state(false);
let totalCount = $state(0);

const eventName = $derived(eventNames[selectedEvent]);

const fetchRankings = async (urlParams: URLSearchParams) => {
	loading = true;
	try {
		const response = await fetchJson<Paginated<RecordInstance>>(`${BASE_URL}/api/rankings/?${urlParams.toString()}`);

		results = response;
		currentPage = pageNum;
		totalCount = response.count;
		hasNext = Boolean(response.next);
		hasPrevious = Boolean(response.previous);
		totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
	} catch (error) {
		console.error("Failed to fetch rankings:", error);
		results = null;
	} finally {
		loading = false;
	}
};

const goToPage = (page: number) => {
	if (page >= 1 && page <= totalPages) {
		pageNum = page;
	}
};

const goToNextPage = () => hasNext && (pageNum = currentPage + 1);

const goToPreviousPage = () => hasPrevious && (pageNum = currentPage - 1);

$effect(() => {
	if (selectedEvent !== previousEvent) {
		previousEvent = selectedEvent;
		if (isSinglePrimaryEvent(selectedEvent)) {
			isAverage = false;
		}
	}
});

$effect(() => {
	// oxlint-disable-next-line @typescript-eslint/no-unused-vars
	const _ = {
		isAverage,
		selectedEvent,
		selectedSession,
		showAllResults,
		uoftStudentStatus,
	};
	pageNum = 1;
});

$effect(() => {
	if (!selectedSession) {
		return;
	}

	const urlParams = new SvelteURLSearchParams({
		all: showAllResults.toString(),
		event: selectedEvent,
		page: pageNum.toString(),
		type: isAverage ? "average" : "single",
	});

	if (selectedSession !== "-1") {
		urlParams.append("session_id", selectedSession);
	}
	if (uoftStudentStatus.length > 0) {
		uoftStudentStatus.forEach((status) => {
			urlParams.append("uoft", status);
		});
	}

	fetchRankings(urlParams);
});
</script>

<svelte:head>
	<title>Rankings | University of Toronto Cube Club</title>
	<meta name="description" content="Rankings for the University of Toronto Rubik's Cube Club." />
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<!-- Header -->
		<div class="mb-6">
			<h1 class="text-2xl font-bold tracking-tight text-main sm:text-3xl">
				Rankings for {eventName}
			</h1>
			<p class="mt-1 text-sm text-secondary">Official club leaderboards by event and student status.</p>
		</div>

		<RankingSelector
			bind:isAverage
			bind:selectedEvent
			bind:showAll={showAllResults}
			bind:session={selectedSession}
			bind:studentStatus={uoftStudentStatus}
		/>

		<div class="mt-6 overflow-x-auto border border-border bg-surface">
			{#if loading}
				<div class="p-12 text-center">
					<LoadingScreen message="Loading Rankings for {eventName}" inline />
				</div>
			{:else if results?.results.length}
				<table class="min-w-full divide-y divide-border">
					<thead class="bg-surface-subtle">
						<tr>
							<th class="w-14 px-4 py-2.5 text-center text-xs font-semibold tracking-wider text-secondary uppercase"
								>#</th
							>
							<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-secondary uppercase">Name</th>
							<th
								class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"
								class:lg:pe-24={!isAverage}>Result</th
							>
							<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-secondary uppercase"
								>Competition</th
							>
							{#if isAverage}
								{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
									<th
										class="hidden px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase md:table-cell"
										>Solve {idx + 1}</th
									>
								{/each}
							{/if}
						</tr>
					</thead>
					<tbody class="divide-y divide-border bg-surface">
						{#each results?.results as result, idx (idx)}
							<tr class="transition-colors hover:bg-surface-muted">
								<td
									class="w-14 px-4 py-3 text-center font-mono text-xs font-semibold whitespace-nowrap text-secondary tabular-nums"
								>
									{result.rank}
								</td>
								<td class="px-4 py-3 text-left text-sm font-medium whitespace-nowrap text-main">
									<a href="/persons/{result.person}" class="transition-colors hover:text-brand hover:underline">
										{result.person_name}
									</a>
								</td>
								<td
									class="px-4 py-3 text-right font-mono text-sm font-bold whitespace-nowrap text-brand tabular-nums"
									class:lg:pe-24={!isAverage}
								>
									{renderTime(result.result)}
								</td>
								<td class="px-4 py-3 text-left text-sm whitespace-nowrap text-secondary">
									<a
										class="transition-colors hover:text-brand hover:underline"
										href="/competitions/{result.competition_id}"
									>
										{result.competition_name}
									</a>
								</td>
								{#if isAverage}
									{#each result.times_list as time, timeIdx (timeIdx)}
										<td
											class="hidden px-4 py-3 text-right font-mono text-sm whitespace-nowrap text-secondary tabular-nums md:table-cell"
										>
											{renderTime(time)}
										</td>
									{/each}
								{/if}
							</tr>
						{/each}
					</tbody>
				</table>
				{#if totalPages > 1}
					<div class="border-t border-border px-4 py-3">
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
				<div class="p-12 text-center text-secondary">
					<h2 class="text-base font-semibold text-main">
						No results found for {eventName}
					</h2>
					<p class="mt-1 text-xs text-secondary">Try selecting a different event or adjusting your filters.</p>
				</div>
			{/if}
		</div>
	</div>
</div>
