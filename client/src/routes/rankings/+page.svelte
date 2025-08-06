<script lang="ts">
	import Backbutton from '$lib/components/Backbutton.svelte';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';
	import PaginationControls from '$lib/components/PaginationControls.svelte';
	import RankingSelector from '$lib/components/RankingSelector.svelte';
	import {
		eventNames,
		eventSolves,
		type Paginated,
		type RecordInstance,
		type WCAEvent
	} from '$lib/types';
	import { BASE_URL, PAGINATION_SIZE, renderTime } from '$lib/utils';

	let selectedEvent: WCAEvent = $state('333');
	let isAverage = $state(false);
	let showAllResults = $state(false);
	let pageNum = $state(1);

	const eventName = $derived(eventNames[selectedEvent]);

	let results: Paginated<RecordInstance> | null = $state(null);
	let loading = $state(true);
	let currentPage = $state(1);
	let totalPages = $state(1);
	let hasNext = $state(false);
	let hasPrevious = $state(false);
	let totalCount = $state(0);

	const fetchRankings = async (urlParams: URLSearchParams) => {
		loading = true;
		try {
			const response = await fetch(`${BASE_URL}/api/rankings/?${urlParams.toString()}`);
			if (!response.ok) throw new Error('Network response was not ok');

			const data: Paginated<RecordInstance> = await response.json();

			results = data;
			currentPage = pageNum;
			totalCount = data.count;
			hasNext = !!data.next;
			hasPrevious = !!data.previous;
			totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
		} catch (error) {
			console.error('Failed to fetch rankings:', error);
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
		// eslint-disable-next-line @typescript-eslint/no-unused-vars
		const _ = { selectedEvent, isAverage, showAllResults };

		return () => {
			pageNum = 1;
		};
	});

	$effect(() => {
		const urlParams = new URLSearchParams({
			event: selectedEvent,
			type: isAverage ? 'average' : 'single',
			all: showAllResults.toString(),
			page: pageNum.toString()
		});
		fetchRankings(urlParams);
	});
</script>

<Backbutton />
<div class="min-h-screen py-8">
	<div class="mx-auto max-w-6xl px-4">
		<!-- Header -->
		<div class="mb-8">
			<h1 class="text-3xl font-bold text-gray-900">Rankings for {eventName}</h1>
		</div>

		<RankingSelector bind:isAverage bind:selectedEvent bind:showAll={showAllResults} />

		<div class="mt-4 overflow-hidden rounded-lg border border-gray-200 bg-white shadow-sm">
			{#if loading}
				<LoadingScreen message={`Loading Rankings for ${eventName}`} inline />
			{:else if results?.results.length}
				<table class="min-w-full divide-y divide-gray-200">
					<thead>
						<tr>
							<th
								class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider text-gray-500"
								>#</th
							>
							<th
								class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500"
								>Name</th
							>
							<th
								class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500"
								class:ps-24={!isAverage}>Result</th
							>
							<th
								class="px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500"
								>Competition</th
							>
							{#if isAverage}
								{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
									<th
										class="hidden px-6 py-3 text-center text-xs font-medium uppercase tracking-wider text-gray-500 md:table-cell"
										>Solve {idx + 1}</th
									>
								{/each}
							{/if}
						</tr>
					</thead>
					<tbody>
						{#each results?.results as result, idx (idx)}
							<tr class="transition-colors duration-100 ease-in-out hover:bg-gray-100">
								<td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900"
									>{(pageNum - 1) * PAGINATION_SIZE + idx + 1}</td
								>
								<td
									class="whitespace-nowrap px-6 py-4 text-center text-sm font-medium text-gray-900"
									>{result.person_name}</td
								>
								<td
									class="whitespace-nowrap px-6 py-4 text-center font-mono text-sm font-bold text-gray-900"
									class:ps-24={!isAverage}>{renderTime(result.result)}</td
								>
								<td class="whitespace-nowrap px-6 py-4 text-center text-sm text-gray-700">
									<a class="hover:text-gray-400" href={`/competitions/${result.competition_id}`}
										>{result.competition_name}</a
									>
								</td>
								{#if isAverage}
									{#each result.times_list as time, timeIdx (timeIdx)}
										<td
											class="hidden whitespace-nowrap px-6 py-4 text-center font-mono text-sm text-gray-700 md:table-cell"
											>{renderTime(time)}</td
										>
									{/each}
								{/if}
							</tr>
						{/each}
					</tbody>
				</table>

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
			{:else}
				<div class="p-8 text-center text-gray-500">
					<h2 class="text-xl font-semibold">No results found for {eventName}</h2>
					<p class="mt-4">Try selecting a different event or adjusting your filters.</p>
				</div>
			{/if}
		</div>
	</div>
</div>
