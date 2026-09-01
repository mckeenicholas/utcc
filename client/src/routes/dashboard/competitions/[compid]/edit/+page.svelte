<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import { page } from "$app/stores";
import DateForm from "$lib/components/DateForm.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import SelectMenu from "$lib/components/SelectMenu.svelte";
import SessionSelector from "$lib/components/SessionSelector.svelte";
import authFetch from "$lib/authFetch";
import { fetchSessions } from "$lib/competitionSessionService";
import { type Competition, type Session, studentDesignatorOptions } from "$lib/types";
import { BASE_URL, checkLoginStatus, fetchJson, toInt } from "$lib/utils";

const id = $page.params.compid;

let competitionData: Competition | null = $state(null);
let isLoading = $state(true);
let currentErrorMessage = $state<string | null>(null);
let selectedEditSession: string = $state("-1");
let sessions: Session[] = $state([]);

onMount(async () => {
	try {
		const [competitionDataResponse, sessionsResponse, loggedIn] = await Promise.all([
			fetchJson<Competition>(`${BASE_URL}/api/competitions/${id}/`),
			fetchSessions(),
			checkLoginStatus(),
		]);

		if (!loggedIn) {
			goto("/dashboard/signin");
		}

		competitionData = competitionDataResponse;
		sessions = sessionsResponse;

		selectedEditSession = competitionData.session ? competitionData.session.toString() : "-1";
	} catch (error) {
		currentErrorMessage = error instanceof Error ? error.message : "An unknown error occurred.";
		console.error(error);
	} finally {
		isLoading = false;
	}
});

const updateCompetitionData = async () => {
	if (!competitionData) {
		return;
	}

	currentErrorMessage = null;

	try {
		const sessionIdToSubmit = selectedEditSession === "-1" ? null : toInt(selectedEditSession);

		const payload = {
			date: competitionData.date,
			name: competitionData.name,
			session: sessionIdToSubmit,
			student_designator: competitionData.student_designator,
		};

		const response = await authFetch(`${BASE_URL}/api/competitions/${id}/`, {
			body: JSON.stringify(payload),
			headers: {
				"Content-Type": "application/json",
			},
			method: "PUT",
		});

		if (!response.ok) {
			const errorData = await response.json().catch(() => ({}));

			const errorMessage = Object.entries(errorData).reduce((prev, [field, msg]) => `${prev}\n${field}: ${msg}`, "");
			throw new Error(errorMessage);
		}

		goto("/dashboard/competitions");
	} catch (error) {
		currentErrorMessage = error instanceof Error ? error.message : "An update error occurred.";
		console.error(error);
	}
};
</script>

{#if isLoading}
	<LoadingScreen message="Loading Competition" />
{:else}
	<div class="min-h-screen py-8">
		<div class="mx-auto max-w-2xl px-4">
			<div class="mb-6 flex flex-col gap-2">
				<a
					href="/dashboard/competitions"
					class="text-xs font-semibold text-uoft-blue transition-colors hover:text-uoft-blue-80"
				>
					&larr; Back to Competitions
				</a>
				<h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Edit Competition</h1>
			</div>

			{#if currentErrorMessage}
				<div class="mb-6 rounded-sm border border-red-200 bg-red-50 p-3 text-xs font-medium text-uoft-warm-red">
					{currentErrorMessage}
				</div>
			{/if}

			{#if competitionData}
				<div class="border border-gray-200 bg-white p-6">
					<h2 class="mb-6 text-base font-bold text-gray-900">Competition Details</h2>

					<div class="space-y-6">
						<div>
							<label for="compname" class="mb-1 block text-xs font-semibold tracking-wider text-gray-700 uppercase">
								Competition Name
							</label>
							<input
								id="compname"
								bind:value={competitionData.name}
								type="text"
								placeholder="Enter competition name"
								class="block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
							/>
						</div>

						<div>
							<DateForm bind:selectedDate={competitionData.date} />
						</div>

						<div>
							<div class="mb-1 block text-xs font-semibold tracking-wider text-gray-700 uppercase">
								Academic Session
							</div>
							<SessionSelector bind:value={selectedEditSession} sessionData={sessions} defaultMessage="No Session" />
						</div>

						<div>
							<label
								for="comp-designator"
								class="mb-1 block text-xs font-semibold tracking-wider text-gray-700 uppercase"
								>Student Designation</label
							>
							<div class="mt-1">
								<SelectMenu bind:value={competitionData.student_designator} options={studentDesignatorOptions} />
							</div>
						</div>

						<!-- Action Buttons -->
						<div class="flex space-x-3 border-t border-gray-100 pt-4">
							<button
								onclick={updateCompetitionData}
								class="inline-flex items-center rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 focus:outline-none"
							>
								Save Changes
							</button>

							<a
								href="/dashboard/competitions"
								class="inline-flex items-center rounded-sm border border-gray-200 bg-white px-4 py-2 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none"
							>
								Cancel
							</a>
						</div>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}
