<script lang="ts">
import { goto } from '$app/navigation';
import { page } from '$app/stores';
import authFetch from '$lib/authFetch';
import { fetchSessions } from '$lib/competitionSessionService';
import DateForm from '$lib/components/DateForm.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import SessionSelector from '$lib/components/SessionSelector.svelte';
import type { Competition, Session } from '$lib/types';
import { BASE_URL, fetchJson } from '$lib/utils';
import { parseDate } from '@internationalized/date';
import { onMount } from 'svelte';

const id = $page.params.compid;

let competitionData: Competition | null = $state(null);
let isLoading = $state(true);
let errorMessage = $state<string | null>(null);
let selectedEditSession: string = $state('-1');
let sessions: Session[] = $state([]);

onMount(async () => {
	try {
		const [competitionDataResponse, sessionsResponse] = await Promise.all([
			fetchJson<Competition>(`${BASE_URL}/api/competitions/${id}/`),
			fetchSessions()
		]);

		competitionData = competitionDataResponse;
		sessions = sessionsResponse;

		selectedEditSession = competitionData.session ? competitionData.session.toString() : '-1';
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
		const sessionIdToSubmit = selectedEditSession === '-1' ? null : parseInt(selectedEditSession);

		const payload = {
			name: competitionData.name,
			date: competitionData.date,
			session: sessionIdToSubmit
		};

		const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
			method: 'PUT',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(payload)
		});

		if (!response.ok) {
			const errorData = await response.json().catch(() => ({}));

			const errorMessage = Object.entries(errorData).reduce(
				(prev, [field, msg]) => `${prev}\n${field}: ${msg}`,
				''
			);
			throw new Error(errorMessage);
		}

		goto('/dashboard/competitions');
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
			<div class="mb-8 flex items-center justify-between">
				<div class="flex items-center space-x-4">
					<a href="/dashboard/competitions">
						<div
							class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
						>
							<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M15 19l-7-7 7-7"
								/>
							</svg>
							Back to Competitions
						</div>
					</a>
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
									d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
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
								class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
							/>
						</div>

						<div>
							<label for="compdate" class="mb-2 block text-sm font-medium text-gray-700">
								Competition Date
							</label>
							<DateForm
								bind:selectedDate={() => parseDate(competitionData!.date), (newDate) => {
								competitionData = { ...competitionData!, date: newDate.toString()}
							}}
							/>
						</div>

						<div>
							<div class="mb-2 block text-sm font-medium text-gray-700">Academic Session</div>
							<SessionSelector
								bind:value={selectedEditSession}
								sessionData={sessions}
								defaultMessage="No Session"
							/>
						</div>

						<!-- Action Buttons -->
						<div class="flex space-x-3 pt-4">
							<button
								onclick={updateCompetitionData}
								class="inline-flex items-center rounded-md bg-green-600 px-4 py-2 text-sm font-medium text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none"
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

							<a href="/dashboard/competitions">
								<div
									class="inline-flex items-center rounded-md bg-gray-600 px-4 py-2 text-sm font-medium text-white hover:bg-gray-700 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
								>
									Cancel
								</div>
							</a>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}
