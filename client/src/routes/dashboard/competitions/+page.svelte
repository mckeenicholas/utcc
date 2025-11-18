<script lang="ts">
import DashboardCompetitionCard from '$lib/components/DashboardCompetitionCard.svelte';
import { goto } from '$app/navigation';
import { onMount } from 'svelte';
import { BASE_URL, checkLoginStatus, PAGINATION_SIZE } from '$lib/utils';
import type { Competition, Paginated, Session } from '$lib/types';
import authFetch from '$lib/authFetch';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import DateForm from '$lib/components/DateForm.svelte';
import DashboardHeader from '$lib/components/DashboardHeader.svelte';
import PaginationControls from '$lib/components/PaginationControls.svelte';
import SessionSelector from '$lib/components/SessionSelector.svelte';
import { fetchSessions } from '$lib/competitionSessionService';

let competitions: Competition[] = $state([]);
let loading = $state(true);
let newCompName = $state('');
let selectedDate = $state<string>(new Date().toISOString().split('T')[0]);
let currentPage = $state(1);
let totalPages = $state(1);
let hasNext = $state(false);
let hasPrevious = $state(false);
let totalCount = $state(0);
let selectedSession = $state('-1');
let createCompSession = $state('-1');
let allSessions: Session[] = $state([]);

$effect(() => {
	if (selectedSession) {
		fetchCompetitions(currentPage, parseInt(selectedSession));
	}
});

const fetchCompetitions = async (page: number = 1, sessionId: number = -1) => {
	loading = true;

	const url = new URL(`${BASE_URL}/api/competitions/`);
	url.searchParams.set('page', page.toString());
	if (sessionId !== -1) url.searchParams.set('session_id', sessionId.toString());

	const competitionRes = await authFetch(url);

	if (competitionRes.ok) {
		const compResJSON: Paginated<Competition> = await competitionRes.json();
		competitions = compResJSON.results.sort(
			(a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()
		);

		currentPage = page;
		totalCount = compResJSON.count;
		hasNext = !!compResJSON.next;
		hasPrevious = !!compResJSON.previous;
		totalPages = Math.ceil(totalCount / PAGINATION_SIZE);

		loading = false;
	} else {
		console.error('Failed to fetch competitions:', competitionRes.statusText);
		loading = false;
	}
};

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto('/dashboard/signin');
	}

	allSessions = await fetchSessions();
});

const goToNextPage = () => {
	if (hasNext) {
		fetchCompetitions(currentPage + 1, parseInt(selectedSession));
	}
};

const goToPreviousPage = () => {
	if (hasPrevious) {
		fetchCompetitions(currentPage - 1, parseInt(selectedSession));
	}
};

const goToPage = (pageNo: number) => {
	if (pageNo >= 1 && pageNo <= totalPages) {
		fetchCompetitions(pageNo, parseInt(selectedSession));
	}
};

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
			fetchCompetitions(currentPage, parseInt(selectedSession));
		} else {
			alert('Failed to delete competition');
		}
	}
};

const createCompetition = async () => {
	const sessionIdToSubmit = createCompSession === '-1' ? null : parseInt(createCompSession);

	const response = await authFetch(`${BASE_URL}/api/competitions/`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ name: newCompName, date: selectedDate, session: sessionIdToSubmit })
	});

	if (response.ok) {
		const newCompetition: Competition = await response.json();
		// Reset form
		newCompName = '';
		selectedDate = '';
		createCompSession = '-1';

		// Using Goto to not trigger a re-request doesn't seem to work here for some reason
		window.location.href = `/dashboard/competitions/${newCompetition.id}`;
	} else {
		alert('Failed to create competition');
	}
};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<DashboardHeader title="Competitions" showBack />

		<div class="mb-8 rounded-lg bg-white p-6 shadow-sm">
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
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
					/>
				</div>
				<div>
					<DateForm bind:selectedDate={selectedDate} />
				</div>
				<div class="mb-1 block text-sm font-medium text-gray-700">Academic Session</div>
				<SessionSelector
					bind:value={createCompSession}
					sessionData={allSessions}
					defaultMessage="No Session"
					class="mt-0"
				/>
				<button
					onclick={createCompetition}
					disabled={!newCompName || !selectedDate}
					class="w-full rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-400"
				>
					Create Competition
				</button>
			</div>
		</div>

		{#if loading}
			<LoadingScreen message="Loading Competitions" inline />
		{:else}
			<div class="mt-4 mb-8">
				<div class="mb-4 flex items-center justify-between">
					<h2 class="ms-2 text-2xl font-semibold text-gray-800">All Competitions</h2>
					<SessionSelector
						bind:value={selectedSession}
						sessionData={allSessions}
						class="shadow-sm"
					/>
				</div>

				{#if competitions.length === 0}
					<div class="rounded-lg bg-white p-6 shadow-sm">
						<p class="text-center text-gray-500">No competitions found for the selected filter.</p>
					</div>
				{:else}
					<div class="grid gap-4">
						{#each competitions as competition (competition.id)}
							<DashboardCompetitionCard
								competition={competition}
								onDeleteCompetition={deleteCompetition}
							/>
						{/each}
					</div>
					{#if totalPages > 1}
						<div class="mt-4 rounded-md bg-white p-4 shadow-sm">
							<PaginationControls
								currentPage={currentPage}
								totalPages={totalPages}
								hasNext={hasNext}
								hasPrevious={hasPrevious}
								totalCount={totalCount}
								itemsPerPage={PAGINATION_SIZE}
								onNext={goToNextPage}
								onPrevious={goToPreviousPage}
								onPageChange={goToPage}
							/>
						</div>
					{/if}
				{/if}
			</div>
		{/if}
	</div>
</div>
