<script lang="ts">
	import DashboardCompetitionCard from '$lib/components/DashboardCompetitionCard.svelte';

	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { BASE_URL, checkLoginStatus, PAGINATION_SIZE } from '$lib/utils';
	import type { Competition, Paginated } from '$lib/types';
	import authFetch from '$lib/authFetch';
	import { type DateValue } from '@internationalized/date';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';
	import AddCompetitionForm from '$lib/components/AddCompetitionForm.svelte';
	import DashboardHeader from '$lib/components/DashboardHeader.svelte';
	import PaginationControls from '$lib/components/PaginationControls.svelte';

	let competitions: Competition[] = $state([]);
	let loading = $state(true);
	let newCompName = $state('');
	let selectedDate = $state<DateValue | undefined>(undefined);
	let currentPage = $state(1);
	let totalPages = $state(1);
	let hasNext = $state(false);
	let hasPrevious = $state(false);
	let totalCount = $state(0);

	const fetchCompetitions = async (page: number = 1) => {
		const competitionRes = await authFetch(`${BASE_URL}/api/competitions/?page=${page}`);

		if (competitionRes.ok) {
			const compResJSON: Paginated<Competition> = await competitionRes.json();
			competitions = compResJSON.results.sort(
				(a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
			);

			// Update pagination state
			currentPage = page;
			totalCount = compResJSON.count;
			hasNext = !!compResJSON.next;
			hasPrevious = !!compResJSON.previous;
			totalPages = Math.ceil(totalCount / PAGINATION_SIZE);

			loading = false;
		} else if (competitionRes.status === 401) {
			goto('/dashboard/signin');
		}
	};

	onMount(async () => {
		const loggedIn = await checkLoginStatus();

		if (!loggedIn) {
			goto('/dashboard/signin');
			return;
		}

		await fetchCompetitions(1);
	});

	const goToNextPage = () => hasNext && fetchCompetitions(currentPage + 1);
	const goToPreviousPage = () => hasPrevious && fetchCompetitions(currentPage - 1);

	const deleteCompetition = async (id: number) => {
		if (confirm('Are you sure you want to delete this competition?')) {
			const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				competitions = competitions.filter((c) => c.id !== id);
			} else {
				alert('Failed to delete competition');
			}
		}
	};

	const createCompetition = async () => {
		if (!selectedDate) {
			alert('Please select a date');
			return;
		}

		const dateString = selectedDate.toString();

		const response = await authFetch(`${BASE_URL}/api/competitions/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ name: newCompName, date: dateString })
		});

		if (response.ok) {
			const newCompetition: Competition = await response.json();
			// Reset form
			newCompName = '';
			selectedDate = undefined;
			// Navigate directly to the new competition
			goto(`/dashboard/competitions/${newCompetition.id}`);
		} else {
			alert('Failed to create competition');
		}
	};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<!-- Header -->
		<DashboardHeader title="Competitions" showBack />

		<!-- Add New Competition Section -->
		<div class="rounded-lg bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-semibold text-gray-800">Add New Competition</h2>
			<div class="space-y-4">
				<div>
					<label for="new-comp-name" class="block text-sm font-medium text-gray-700"
						>Competition Name</label
					>
					<input
						id="new-comp-name"
						placeholder="Enter competition name"
						bind:value={newCompName}
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
					/>
				</div>
				<div>
					<AddCompetitionForm bind:selectedDate />
				</div>
				<button
					onclick={createCompetition}
					disabled={!newCompName || !selectedDate}
					class="w-full rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400"
				>
					Create Competition
				</button>
			</div>
		</div>

		{#if loading}
			<LoadingScreen message="Loading Competitions" inline />
		{:else}
			<!-- Competitions Section -->
			<div class="mb-8 mt-4">
				<h2 class="mb-4 ms-2 text-2xl font-semibold text-gray-800">Competitions</h2>

				{#if competitions.length === 0}
					<div class="rounded-lg bg-white p-6 shadow-sm">
						<p class="text-center text-gray-500">No competitions added yet</p>
					</div>
				{:else}
					<div class="grid gap-4">
						{#each competitions as competition (competition.id)}
							<DashboardCompetitionCard {competition} onDeleteCompetition={deleteCompetition} />
						{/each}
					</div>
					<div class="mt-4 rounded-md shadow-sm">
						<PaginationControls
							{currentPage}
							{totalPages}
							{hasNext}
							{hasPrevious}
							{totalCount}
							itemsPerPage={PAGINATION_SIZE}
							onNext={goToNextPage}
							onPrevious={goToPreviousPage}
							onPageChange={(pageNo) => fetchCompetitions(pageNo)}
						/>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
