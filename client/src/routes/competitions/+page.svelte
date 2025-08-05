<script lang="ts">
	import type { Competition, Paginated } from '$lib/types';
	import { BASE_URL, PAGINATION_SIZE } from '$lib/utils';
	import { onMount } from 'svelte';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';
	import CompetitionCard from '$lib/components/CompetitionCard.svelte';
	import Backbutton from '$lib/components/Backbutton.svelte';
	import PaginationControls from '$lib/components/PaginationControls.svelte';

	let competitions: Competition[] = $state([]);
	let loading = $state(true);
	let error = $state<string | null>(null);
	let currentPage = $state(1);
	let totalPages = $state(1);
	let hasNext = $state(false);
	let hasPrevious = $state(false);
	let totalCount = $state(0);

	const fetchCompetitions = async (page: number = 1) => {
		loading = true;
		error = null;

		try {
			const response = await fetch(`${BASE_URL}/api/competitions?page=${page}`);

			if (!response.ok) {
				throw new Error('Failed to fetch competitions');
			}

			const data: Paginated<Competition> = await response.json();

			competitions = data.results;
			currentPage = page;
			totalCount = data.count;
			hasNext = !!data.next;
			hasPrevious = !!data.previous;
			totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
		} catch (err) {
			console.error('Error fetching competitions:', err);
			error = 'Failed to load competitions. Please try again later.';
		} finally {
			loading = false;
		}
	};

	onMount(() => {
		fetchCompetitions(1);
	});

	const goToNextPage = () => {
		if (hasNext) {
			fetchCompetitions(currentPage + 1);
		}
	};

	const goToPreviousPage = () => {
		if (hasPrevious) {
			fetchCompetitions(currentPage - 1);
		}
	};

	const goToPage = (page: number) => {
		if (page >= 1 && page <= totalPages) {
			fetchCompetitions(page);
		}
	};
</script>

<Backbutton />
{#if loading}
	<LoadingScreen message="Loading Competitions" />
{:else}
	<div class="min-h-screen bg-gray-50 py-8">
		<div class="mx-auto max-w-6xl px-4">
			<!-- Error State -->
			{#if error}
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
					<p class="mt-2 text-red-700">{error}</p>
					<button
						onclick={() => window.location.reload()}
						class="mt-4 inline-flex items-center rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
					>
						Try Again
					</button>
				</div>
			{:else if competitions.length > 0}
				<h1 class="mb-8 ms-2 text-3xl font-bold text-gray-900">All Competitions</h1>
				<!-- Competitions List -->
				<div class="space-y-4">
					{#each competitions as competition (competition.id)}
						<CompetitionCard {competition} />
					{/each}
				</div>

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
					<p class="mt-2 text-gray-600">There are no competitions to display at this time.</p>
				</div>
			{/if}
		</div>
	</div>
{/if}
