<script lang="ts">
import { onMount } from 'svelte';
import { page } from '$app/stores';
import type { CompetitionResults, Result, WCAEvent, User } from '$lib/types';
import { BASE_URL, checkLoginStatus, fetchJson } from '$lib/utils';
import authFetch from '$lib/authFetch';
import ResultForm from '$lib/components/ResultForm.svelte';
import ResultsTable from '$lib/components/ResultsTable.svelte';
import PageHeader from '$lib/components/PageHeader.svelte';
import ErrorMessage from '$lib/components/ErrorMessage.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import UserSearch from '$lib/components/UserSearch.svelte';
import CreateUserModal from '$lib/components/CreateUserModal.svelte';
import { goto } from '$app/navigation';

const compId = $page.params.compid;

let competitionResults: CompetitionResults | null = $state(null);
let loading = $state(true);
let submitting = $state(false);
let errorMessage = $state<string | null>(null);
let editingResult: Result | null = $state(null);
let showCreateUserModal = $state(false);
let newUserName = $state('');
let userInputRawValue = $state('');

let selectedPersonId: number | null = $state(null);
let selectedPersonName = $state('');

let formData = $state({
	event: '333' as WCAEvent,
	round: 1,
	time1: 0,
	time2: 0,
	time3: 0,
	time4: 0,
	time5: 0
});

const fetchData = async (background = true) => {
	loading = background;
	try {
		const [results, loggedIn] = await Promise.all([
			fetchJson<CompetitionResults>(`${BASE_URL}/api/competitions/${compId}/results/`),
			checkLoginStatus()
		]);

		if (!loggedIn) {
			goto('/dashboard/signin');
		}

		competitionResults = results;
	} catch {
		errorMessage = 'Failed to load competition data.';
	} finally {
		loading = false;
	}
};

onMount(fetchData);

const findResult = (personId: number, event: WCAEvent, round: number) => {
	if (!competitionResults) return null;

	const eventResult = competitionResults.results.find((er) => er.event === event);
	if (!eventResult) return null;

	const roundResult = eventResult.rounds.find((r) => r.round === round);
	if (!roundResult) return null;

	return roundResult.results.find((r) => r.person === personId);
};

$effect(() => {
	if (!selectedPersonId || !competitionResults) {
		resetFormTimes();
		editingResult = null;
		return;
	}

	const existing = findResult(selectedPersonId, formData.event, formData.round);
	if (existing) {
		formData.time1 = existing.times[0] || 0;
		formData.time2 = existing.times[1] || 0;
		formData.time3 = existing.times[2] || 0;
		formData.time4 = existing.times[3] || 0;
		formData.time5 = existing.times[4] || 0;
		// Convert to the Result format for editing
		editingResult = {
			id: existing.id,
			person_name: existing.person_name,
			person: existing.person,
			competition: Number(compId),
			event: formData.event,
			round: formData.round,
			time1: existing.times[0] || 0,
			time2: existing.times[1] || 0,
			time3: existing.times[2] || 0,
			time4: existing.times[3] || 0,
			time5: existing.times[4] || 0,
			single: existing.single,
			average: existing.average
		};
	} else {
		resetFormTimes();
		editingResult = null;
	}
});

const handleUserSelect = (user: User) => {
	selectedPersonId = user.id;
	selectedPersonName = user.name;
};

const handleClearUser = () => {
	selectedPersonId = null;
	selectedPersonName = '';
	userInputRawValue = '';
};

const handleAddUser = () => {
	newUserName = userInputRawValue;
	showCreateUserModal = true;
};

const handleUserCreated = (user: User) => {
	handleUserSelect(user);
};

const submitResult = async () => {
	if (!selectedPersonId) {
		errorMessage = 'Please select a user';
		return;
	}
	submitting = true;
	const url = editingResult
		? `${BASE_URL}/api/results/${editingResult.id}/`
		: `${BASE_URL}/api/results/`;
	const method = editingResult ? 'PUT' : 'POST';

	try {
		await authFetch(url, {
			method,
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				...formData,
				person: selectedPersonId,
				competition: Number(compId)
			})
		});
		resetForm();
		await fetchData(false);
	} catch {
		errorMessage = 'Failed to submit result.';
	} finally {
		submitting = false;
	}
};

const editResult = (result: Result) => {
	window.scrollTo({ top: 0, behavior: 'smooth' });

	editingResult = result;
	selectedPersonId = result.person;
	selectedPersonName = result.person_name;
	formData = { ...formData, ...result };
};

const deleteResult = async (resultId: number) => {
	if (!confirm('Are you sure?')) return;
	try {
		await authFetch(`${BASE_URL}/api/results/${resultId}/`, { method: 'DELETE' });
		await fetchData(true);
	} catch {
		errorMessage = 'Failed to delete result.';
	}
};

const resetForm = () => {
	handleClearUser();
	resetFormTimes();
	editingResult = null;
};

const resetFormTimes = () => {
	formData.time1 = 0;
	formData.time2 = 0;
	formData.time3 = 0;
	formData.time4 = 0;
	formData.time5 = 0;
};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-[1500px] px-4">
		<PageHeader
			competition={competitionResults?.competition ?? null}
			backText="Back to competitions"
			backUrl="/dashboard/competitions"
		/>
		<ErrorMessage message={errorMessage} />

		<div class="grid grid-cols-1 gap-8 lg:grid-cols-4">
			<div class="lg:col-span-1">
				<div class="rounded-lg bg-white p-6 shadow-sm">
					<h3 class="mb-4 text-lg font-semibold">Select User</h3>
					<UserSearch
						value={selectedPersonName}
						onSelect={handleUserSelect}
						onClear={handleClearUser}
						onAddUser={handleAddUser}
						isEditMode={editingResult != null}
						userSelected={selectedPersonId != null}
						bind:searchTerm={userInputRawValue}
					/>

					<ResultForm
						bind:formData={formData}
						editingResult={editingResult}
						submitting={submitting}
						onSubmit={submitResult}
						onCancel={resetForm}
					/>
				</div>
			</div>
			<div class="lg:col-span-3">
				{#if loading}
					<LoadingScreen message="Loading Competition Data" inline />
				{:else}
					<ResultsTable
						competitionResults={competitionResults}
						onEdit={editResult}
						onDelete={deleteResult}
					/>
				{/if}
			</div>
		</div>
	</div>
</div>

<CreateUserModal
	show={showCreateUserModal}
	initialName={newUserName}
	onClose={() => (showCreateUserModal = false)}
	onUserCreated={handleUserCreated}
/>
