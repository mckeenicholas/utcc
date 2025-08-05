<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import type { Competition, CompetitionResults, Result, WCAEvent, User } from '$lib/types';
	import { BASE_URL } from '$lib/utils';
	import authFetch from '$lib/authFetch';
	import ResultForm from '$lib/components/ResultForm.svelte';
	import ResultsTable from '$lib/components/ResultsTable.svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';
	import UserSearch from '$lib/components/UserSearch.svelte';
	import CreateUserModal from '$lib/components/CreateUserModal.svelte';

	const compId = $page.params.compid;

	let competition: Competition | null = $state(null);
	let results: Result[] = $state([]);
	let loading = $state(true);
	let submitting = $state(false);
	let errorMessage = $state<string | null>(null);
	let editingResult: Result | null = $state(null);
	let showCreateUserModal = $state(false);
	let newUserName = $state('');

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

	const fetchData = async () => {
		loading = true;
		try {
			const compResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/`);
			competition = await compResponse.json();

			const resultsResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/results/`);
			const resultsData: CompetitionResults = await resultsResponse.json();
			results = (resultsData.results || []).flatMap((eventResult) =>
				eventResult.rounds.flatMap((round) =>
					round.results.map((person) => ({
						id: person.id,
						person_name: person.person_name,
						person_id: person.person_id,
						competition: Number(compId),
						event: eventResult.event,
						round: round.round,
						time1: person.times[0] || 0,
						time2: person.times[1] || 0,
						time3: person.times[2] || 0,
						time4: person.times[3] || 0,
						time5: person.times[4] || 0,
						single: person.single,
						average: person.average
					}))
				)
			);
		} catch {
			errorMessage = 'Failed to load competition data.';
		} finally {
			loading = false;
		}
	};

	onMount(fetchData);

	$effect(() => {
		if (!selectedPersonId) {
			resetFormTimes();
			editingResult = null;
			return;
		}
		const existing = results.find(
			(r) =>
				r.person_id === selectedPersonId && r.event === formData.event && r.round === formData.round
		);
		if (existing) {
			formData.time1 = existing.time1;
			formData.time2 = existing.time2;
			formData.time3 = existing.time3;
			formData.time4 = existing.time4;
			formData.time5 = existing.time5;
			editingResult = existing;
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
	};

	const handleAddUser = () => {
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
					person_id: selectedPersonId,
					competition: Number(compId)
				})
			});
			resetForm();
			await fetchData();
		} catch {
			errorMessage = 'Failed to submit result.';
		} finally {
			submitting = false;
		}
	};

	const editResult = (result: Result) => {
		editingResult = result;
		selectedPersonId = result.person_id;
		selectedPersonName = result.person_name;
		formData = { ...formData, ...result };
		document.querySelector('.submit-form')?.scrollIntoView({ behavior: 'smooth' });
	};

	const deleteResult = async (resultId: number) => {
		if (!confirm('Are you sure?')) return;
		try {
			await authFetch(`${BASE_URL}/api/results/${resultId}/`, { method: 'DELETE' });
			await fetchData();
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

{#if loading}
	<LoadingScreen message="Loading Competition" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-[1500px] px-4">
			<PageHeader {competition} />
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
						/>

						{#if editingResult}
							<div class="mt-4">
								<p>Editing: {editingResult.person_name}</p>
								<button onclick={resetForm}>Cancel Edit</button>
							</div>
						{/if}

						<ResultForm
							bind:formData
							{editingResult}
							{submitting}
							onSubmit={submitResult}
							onCancel={resetForm}
						/>
					</div>
				</div>

				<div class="lg:col-span-3">
					<ResultsTable {results} onEdit={editResult} onDelete={deleteResult} />
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
{/if}
