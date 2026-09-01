<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import DashboardCompetitionCard from "$lib/components/DashboardCompetitionCard.svelte";
import DashboardHeader from "$lib/components/DashboardHeader.svelte";
import DateForm from "$lib/components/DateForm.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PaginationControls from "$lib/components/PaginationControls.svelte";
import SelectMenu from "$lib/components/SelectMenu.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import authFetch from "$lib/authFetch";
import { fetchSessions } from "$lib/competitionSessionService";
import { type Competition, type Paginated, type Session, studentDesignatorOptions } from "$lib/types";
import { BASE_URL, PAGINATION_SIZE, checkLoginStatus, toInt } from "$lib/utils";

let competitions: Competition[] = $state([]);
let loading = $state(true);
let newCompName = $state("");
let selectedDate = $state<string>(new Date().toISOString().split("T")[0]);
let currentPage = $state(1);
let totalPages = $state(1);
let hasNext = $state(false);
let hasPrevious = $state(false);
let totalCount = $state(0);
let selectedSession = $state("-1");
let createCompSession = $state("-1");
let createCompDesignator = $state("UTSG");
let allSessions: Session[] = $state([]);

$effect(() => {
	if (selectedSession) {
		fetchCompetitions(currentPage, toInt(selectedSession) ?? -1);
	}
});

const fetchCompetitions = async (page = 1, sessionId = -1) => {
	loading = true;

	const url = new URL(`${BASE_URL}/api/competitions/`);
	url.searchParams.set("page", page.toString());
	if (sessionId !== -1) {
		url.searchParams.set("session_id", sessionId.toString());
	}

	const competitionRes = await authFetch(url);

	if (competitionRes.ok) {
		const compResJSON: Paginated<Competition> = await competitionRes.json();
		competitions = compResJSON.results.toSorted((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());

		currentPage = page;
		totalCount = compResJSON.count;
		hasNext = Boolean(compResJSON.next);
		hasPrevious = Boolean(compResJSON.previous);
		totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
	} else {
		console.error("Failed to fetch competitions:", competitionRes.statusText);
	}
	loading = false;
};

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto("/dashboard/signin");
	}

	allSessions = await fetchSessions();
});

const goToNextPage = () => {
	if (hasNext) {
		fetchCompetitions(currentPage + 1, toInt(selectedSession) ?? -1);
	}
};

const goToPreviousPage = () => {
	if (hasPrevious) {
		fetchCompetitions(currentPage - 1, toInt(selectedSession) ?? -1);
	}
};

const goToPage = (pageNo: number) => {
	if (pageNo >= 1 && pageNo <= totalPages) {
		fetchCompetitions(pageNo, toInt(selectedSession) ?? -1);
	}
};

const deleteCompetition = async (id: number) => {
	if (confirm("Are you sure you want to delete this competition?")) {
		const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
			headers: {
				"Content-Type": "application/json",
			},
			method: "DELETE",
		});

		if (response.ok) {
			competitions = competitions.filter((c) => c.id !== id);
			fetchCompetitions(currentPage, toInt(selectedSession) ?? -1);
		} else {
			alert("Failed to delete competition");
		}
	}
};

const createCompetition = async () => {
	const sessionIdToSubmit = createCompSession === "-1" ? null : toInt(createCompSession);

	const response = await authFetch(`${BASE_URL}/api/competitions/`, {
		body: JSON.stringify({
			date: selectedDate,
			name: newCompName,
			session: sessionIdToSubmit,
			student_designator: createCompDesignator,
		}),
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
	});

	if (response.ok) {
		const newCompetition: Competition = await response.json();
		// Reset form
		newCompName = "";
		selectedDate = "";
		createCompSession = "-1";
		createCompDesignator = "UTSG";

		// Using Goto to not trigger a re-request doesn't seem to work here for some reason
		globalThis.location.href = `/dashboard/competitions/${newCompetition.id}`;
	} else {
		alert("Failed to create competition");
	}
};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<div class="mb-6">
			<DashboardHeader title="Competitions" showBack />
		</div>

		<div class="mb-6 border border-gray-200 bg-white p-6">
			<h2 class="mb-4 text-base font-bold text-gray-900">Add New Competition</h2>
			<div class="space-y-4">
				<div>
					<label for="new-comp-name" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase"
						>Competition Name</label
					>
					<input
						id="new-comp-name"
						placeholder="Enter competition name"
						bind:value={newCompName}
						class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
					/>
				</div>
				<div>
					<DateForm bind:selectedDate />
				</div>
				<div class="mb-1 block text-xs font-semibold tracking-wider text-gray-700 uppercase">Academic Session</div>
				<SessionSelector
					bind:value={createCompSession}
					sessionData={allSessions}
					defaultMessage="No Session"
					class="mt-0"
				/>
				<div>
					<label for="new-comp-designator" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase"
						>Student Designation</label
					>
					<div class="mt-1">
						<SelectMenu bind:value={createCompDesignator} options={studentDesignatorOptions} />
					</div>
				</div>
				<button
					onclick={createCompetition}
					disabled={!newCompName || !selectedDate}
					class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 disabled:opacity-50"
				>
					Create Competition
				</button>
			</div>
		</div>

		{#if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen message="Loading Competitions..." inline minHeight="10rem" />
			</div>
		{:else}
			<div class="mt-6 mb-8">
				<div class="mb-4 flex items-center justify-between border-b border-gray-200 pb-2">
					<span class="text-xs font-semibold tracking-wider text-gray-700 uppercase">All Competitions</span>
					<SessionSelector bind:value={selectedSession} sessionData={allSessions} />
				</div>

				{#if competitions.length === 0}
					<div class="border border-gray-200 bg-white p-12 text-center text-xs text-gray-700">
						No competitions found for the selected filter.
					</div>
				{:else}
					<div class="grid gap-3">
						{#each competitions as competition (competition.id)}
							<DashboardCompetitionCard {competition} onDeleteCompetition={deleteCompetition} />
						{/each}
					</div>
					{#if totalPages > 1}
						<div class="mt-4 border border-gray-200 bg-white p-4">
							<PaginationControls
								{currentPage}
								{totalPages}
								{hasNext}
								{hasPrevious}
								{totalCount}
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
