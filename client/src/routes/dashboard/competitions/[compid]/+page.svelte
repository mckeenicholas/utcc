<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import type { Competition, CompetitionResults, Result, WCAEvent } from '$lib/types';
	import { BASE_URL } from '$lib/utils';
	import authFetch from '$lib/authFetch';
	import ResultForm from '$lib/components/ResultForm.svelte';
	import ResultsTable from '$lib/components/ResultsTable.svelte';
	import PageHeader from '$lib/components/PageHeader.svelte';
	import ErrorMessage from '$lib/components/ErrorMessage.svelte';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';

	const compId = $page.params.compid;

	let competition: Competition | null = $state(null);
	let results: Result[] = $state([]);
	let loading = $state(true);
	let submitting = $state(false);
	let errorMessage = $state<string | null>(null);
	let editingResult: Result | null = $state(null);

	// Form state
	let formData = $state({
		name: '',
		event: '333' as WCAEvent,
		round: 1,
		time1: 0,
		time2: 0,
		time3: 0,
		time4: 0,
		time5: 0
	});

	const fetchData = async () => {
		try {
			// Fetch competition details
			const compResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/`);
			if (!compResponse.ok) throw new Error('Failed to fetch competition');
			competition = await compResponse.json();

			// Fetch results for this competition
			const resultsResponse = await fetch(`${BASE_URL}/api/competitions/${compId}/results/`);
			if (!resultsResponse.ok) throw new Error('Failed to fetch results');
			const resultsData: CompetitionResults = await resultsResponse.json();

			// Flatten the results from the nested structure
			results = (resultsData.results || []).flatMap((eventResult) =>
				eventResult.rounds.flatMap((round) =>
					round.results.map((person) => ({
						id: person.id,
						name: person.name,
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
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'An error occurred';
			console.error(error);
		} finally {
			loading = false;
		}
	};

	const submitResult = async () => {
		if (!formData.name.trim()) {
			errorMessage = 'Please enter a name';
			return;
		}

		submitting = true;
		errorMessage = null;

		try {
			const url = editingResult
				? `${BASE_URL}/api/results/${editingResult.id}/`
				: `${BASE_URL}/api/results/`;

			const method = editingResult ? 'PUT' : 'POST';

			const response = await authFetch(url, {
				method,
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					...formData,
					competition: Number(compId)
				})
			});

			if (!response.ok) {
				const errorData = await response.json().catch(() => ({
					message: editingResult ? 'Failed to update result' : 'Failed to submit result'
				}));
				throw new Error(
					errorData.message ||
						(editingResult ? 'Failed to update result' : 'Failed to submit result')
				);
			}

			// Reset form and editing state
			resetForm();

			// Refresh results
			await fetchData();
		} catch (error) {
			errorMessage =
				error instanceof Error
					? error.message
					: editingResult
						? 'Failed to update result'
						: 'Failed to submit result';
			console.error(error);
		} finally {
			submitting = false;
		}
	};

	const resetForm = () => {
		formData = {
			name: '',
			event: '333' as WCAEvent,
			round: 1,
			time1: 0,
			time2: 0,
			time3: 0,
			time4: 0,
			time5: 0
		};
		editingResult = null;
	};

	const editResult = (result: Result) => {
		editingResult = result;
		formData = {
			name: result.name,
			event: result.event,
			round: result.round,
			time1: result.time1,
			time2: result.time2,
			time3: result.time3,
			time4: result.time4,
			time5: result.time5
		};

		// Scroll to form
		document.querySelector('.submit-form')?.scrollIntoView({ behavior: 'smooth' });
	};

	const cancelEdit = () => {
		resetForm();
	};

	const deleteResult = async (resultId: number) => {
		if (!confirm('Are you sure you want to delete this result?')) return;

		try {
			const response = await authFetch(`${BASE_URL}/api/results/${resultId}/`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				throw new Error('Failed to delete result');
			}

			await fetchData();
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'Failed to delete result';
			console.error(error);
		}
	};

	const handleFormDataChange = (key: string, value: unknown) => {
		formData = { ...formData, [key]: value };
	};

	onMount(fetchData);
</script>

{#if loading}
	<LoadingScreen message="Loading Competition" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-[1500px] px-4">
			<!-- Header with Navigation -->
			<PageHeader {competition} />

			<!-- Error Message -->
			<ErrorMessage message={errorMessage} />

			<!-- Main Content Layout: Form on Left, Results on Right (Desktop) / Stacked (Mobile) -->
			<div class="grid grid-cols-1 gap-8 lg:grid-cols-4">
				<!-- Submit Result Form -->
				<div class="lg:col-span-1">
					<ResultForm
						{formData}
						{editingResult}
						{submitting}
						onSubmit={submitResult}
						onCancel={cancelEdit}
						onFormDataChange={handleFormDataChange}
					/>
				</div>

				<!-- Results Table -->
				<div class="lg:col-span-3">
					<ResultsTable {results} onEdit={editResult} onDelete={deleteResult} />
				</div>
			</div>
		</div>
	</div>
{/if}
