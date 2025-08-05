<script lang="ts">
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import authFetch from '$lib/authFetch';
	import LoadingScreen from '$lib/components/LoadingScreen.svelte';
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
	<LoadingScreen message="Loading Competition" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-2xl px-4">
			<!-- Header with Navigation -->
			<div class="mb-8 flex items-center justify-between">
				<div class="flex items-center space-x-4">
					<button
						onclick={() => goto('/dashboard')}
						class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
					>
						<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M15 19l-7-7 7-7"
							/>
						</svg>
						Back to Dashboard
					</button>
					<h1 class="text-3xl font-bold text-gray-900">Edit Competition</h1>
				</div>
			</div>

			{#if errorMessage}
				<div class="mb-6 rounded-md border border-red-200 bg-red-50 p-4">
					<div class="flex">
						<div class="flex-shrink-0">
							<svg
								class="h-5 w-5 text-red-400"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
								/>
							</svg>
						</div>
						<div class="ml-3">
							<h3 class="text-sm font-medium text-red-800">Error</h3>
							<div class="mt-2 text-sm text-red-700">
								{errorMessage}
							</div>
						</div>
					</div>
				</div>
			{/if}

			{#if competitionData}
				<!-- Edit Form -->
				<div class="rounded-lg bg-white p-6 shadow-sm">
					<h2 class="mb-6 text-xl font-semibold text-gray-800">Competition Details</h2>

					<div class="space-y-6">
						<div>
							<label for="compname" class="mb-2 block text-sm font-medium text-gray-700">
								Competition Name
							</label>
							<input
								id="compname"
								bind:value={competitionData.name}
								type="text"
								placeholder="Enter competition name"
								class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
							/>
						</div>

						<div>
							<label for="compdate" class="mb-2 block text-sm font-medium text-gray-700">
								Competition Date
							</label>
							<input
								id="compdate"
								type="date"
								bind:value={competitionData.date}
								class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
							/>
						</div>

						<!-- Action Buttons -->
						<div class="flex space-x-3 pt-4">
							<button
								onclick={updateCompetitionData}
								class="inline-flex items-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
							>
								<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										stroke-width="2"
										d="M5 13l4 4L19 7"
									/>
								</svg>
								Save Changes
							</button>

							<button
								onclick={() => goto('/dashboard')}
								class="inline-flex items-center rounded-md bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
							>
								Cancel
							</button>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}
