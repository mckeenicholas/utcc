<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import authFetch from '$lib/authFetch';
	import type { Competition } from '$lib/types';
	import { BASE_URL } from '$lib/utils';
	import { onMount } from 'svelte';

	const id = $page.params.compid;

	let competitionData: Competition | null = $state(null);
	let isLoading = $state(true);
	let errorMessage = $state<string | null>(null);

	onMount(async () => {
		try {
			const response = await fetch(`${BASE_URL}/api/competitions/${id}/`);
			if (!response.ok) {
				throw new Error('Failed to fetch competition data.');
			}
			competitionData = await response.json();
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'An unknown error occurred.';
			console.error(error);
		} finally {
			isLoading = false;
		}
	});

	const updateCompetitionData = async () => {
		if (!competitionData) return;

		errorMessage = null;

		try {
			const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(competitionData)
			});

			if (!response.ok) {
				const errorData = await response
					.json()
					.catch(() => ({ message: 'Failed to update competition.' }));
				throw new Error(errorData.message);
			}

			goto('/dashboard');
		} catch (error) {
			errorMessage = error instanceof Error ? error.message : 'An update error occurred.';
			console.error(error);
		}
	};
</script>

{#if isLoading}
	<p class="text-center">Loading...</p>
{:else if errorMessage}
	<div class="col-span-full rounded-md bg-red-100 p-3 text-center text-red-800">
		{errorMessage}
	</div>
{:else if competitionData}
	<div class="grid max-w-lg grid-cols-[auto_1fr] items-center gap-4">
		<label for="compname" class="font-bold">Name:</label>
		<input
			id="compname"
			bind:value={competitionData.name}
			type="text"
			class="rounded-md border border-gray-300 p-2"
		/>

		<label for="compdate" class="font-bold">Date:</label>
		<input
			id="compdate"
			type="date"
			bind:value={competitionData.date}
			class="rounded-md border border-gray-300 p-2"
		/>

		<button
			onclick={updateCompetitionData}
			class="col-start-2 justify-self-start rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
		>
			Update
		</button>
	</div>
{/if}
