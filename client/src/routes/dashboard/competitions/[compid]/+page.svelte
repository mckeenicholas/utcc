<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import { page } from "$app/stores";
import CreateUserModal from "$lib/components/CreateUserModal.svelte";
import ErrorMessage from "$lib/components/ErrorMessage.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PageHeader from "$lib/components/PageHeader.svelte";
import ResultForm from "$lib/components/ResultForm.svelte";
import ResultsTable from "$lib/components/ResultsTable.svelte";
import UserSearch from "$lib/components/UserSearch.svelte";
import { Select } from "bits-ui";
import authFetch from "$lib/authFetch";
import { eventNames, type CompetitionResults, type Result, type User, type WCAEvent } from "$lib/types";
import { BASE_URL, checkLoginStatus, fetchJson } from "$lib/utils";

const compId = $page.params.compid;

let competitionResults: CompetitionResults | null = $state(null);
let loading = $state(true);
let submitting = $state(false);
let errorMessage = $state<string | null>(null);
let editingResult: Result | null = $state(null);
let showCreateUserModal = $state(false);
let newUserName = $state("");
let userInputRawValue = $state("");

let selectedPersonId: number | null = $state(null);
let selectedPersonName = $state("");

let formData = $state({
	event: "333" as WCAEvent,
	round: 1,
	time1: 0,
	time2: 0,
	time3: 0,
	time4: 0,
	time5: 0,
});

const eventOptions = Object.entries(eventNames).map(([key, name]) => ({
	label: name,
	value: key,
}));

const selectedEventLabel = $derived.by(() => {
	const selected = eventOptions.find((option) => option.value === formData.event);
	return selected ? selected.label : "Select an event";
});

const fetchData = async (background = true) => {
	loading = background;
	try {
		const [results, loggedIn] = await Promise.all([
			fetchJson<CompetitionResults>(`${BASE_URL}/api/competitions/${compId}/results/`),
			checkLoginStatus(),
		]);

		if (!loggedIn) {
			goto("/dashboard/signin");
		}

		competitionResults = results;
	} catch {
		errorMessage = "Failed to load competition data.";
	} finally {
		loading = false;
	}
};

onMount(fetchData);

const findResult = (personId: number, event: WCAEvent, round: number) => {
	if (!competitionResults) {
		return null;
	}

	const eventResult = competitionResults.results.find((er) => er.event === event);
	if (!eventResult) {
		return null;
	}

	const roundResult = eventResult.rounds.find((r) => r.round === round);
	if (!roundResult) {
		return null;
	}

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
			average: existing.average,
			competition: Number(compId),
			event: formData.event,
			id: existing.id,
			person: existing.person,
			person_name: existing.person_name,
			round: formData.round,
			single: existing.single,
			time1: existing.times[0] || 0,
			time2: existing.times[1] || 0,
			time3: existing.times[2] || 0,
			time4: existing.times[3] || 0,
			time5: existing.times[4] || 0,
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
	selectedPersonName = "";
	userInputRawValue = "";
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
		errorMessage = "Please select a user";
		return;
	}
	submitting = true;
	const url = editingResult ? `${BASE_URL}/api/results/${editingResult.id}/` : `${BASE_URL}/api/results/`;
	const method = editingResult ? "PUT" : "POST";

	try {
		await authFetch(url, {
			body: JSON.stringify({
				...formData,
				competition: Number(compId),
				person: selectedPersonId,
			}),
			headers: { "Content-Type": "application/json" },
			method,
		});
		resetForm();
		await fetchData(false);
	} catch {
		errorMessage = "Failed to submit result.";
	} finally {
		submitting = false;
	}
};

const editResult = (result: Result) => {
	window.scrollTo({ behavior: "smooth", top: 0 });

	editingResult = result;
	selectedPersonId = result.person;
	selectedPersonName = result.person_name;
	formData = { ...formData, ...result };
};

const deleteResult = async (resultId: number) => {
	if (!confirm("Are you sure?")) {
		return;
	}
	try {
		await authFetch(`${BASE_URL}/api/results/${resultId}/`, { method: "DELETE" });
		await fetchData(true);
	} catch {
		errorMessage = "Failed to delete result.";
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
					<h2 class="mb-4 text-lg font-semibold text-gray-800">
						{editingResult ? "Edit Results" : "Enter Results"}
					</h2>

					<div class="space-y-4">
						<div>
							<label for="event" class="mb-2 block text-sm font-medium text-gray-700">Event</label>
							<Select.Root items={eventOptions} bind:value={formData.event} type="single">
								<Select.Trigger
									class="flex w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-left shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
									aria-label="Select an event"
								>
									<span>{selectedEventLabel}</span>
									<svg
										class="ml-2 h-4 w-4 shrink-0 text-gray-400"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
									</svg>
								</Select.Trigger>
								<Select.Portal>
									<Select.Content
										class="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 z-50 max-h-96 w-[var(--bits-select-anchor-width)] min-w-[var(--bits-select-anchor-width)] overflow-hidden rounded-md border border-gray-200 bg-white py-1 shadow-lg"
										sideOffset={4}
									>
										<Select.Viewport class="p-1">
											{#each eventOptions as option (option.value)}
												<Select.Item
													class="relative flex w-full cursor-default items-center rounded-sm py-1.5 pr-2 pl-8 text-sm outline-none select-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:pointer-events-none data-[disabled]:opacity-50 data-[highlighted]:bg-gray-100"
													value={option.value}
													label={option.label}
												>
													{#snippet children({ selected })}
														{#if selected}
															<span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
																<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
																	<path
																		stroke-linecap="round"
																		stroke-linejoin="round"
																		stroke-width="2"
																		d="M5 13l4 4L19 7"
																	/>
																</svg>
															</span>
														{/if}
														{option.label}
													{/snippet}
												</Select.Item>
											{/each}
										</Select.Viewport>
									</Select.Content>
								</Select.Portal>
							</Select.Root>
						</div>

						<div>
							<label for="round" class="mb-2 block text-sm font-medium text-gray-700">Round</label>
							<input
								id="round"
								type="number"
								min="1"
								bind:value={formData.round}
								class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
							/>
						</div>

						<div>
							<h3 class="mb-2 text-sm font-medium text-gray-700">Select User</h3>
							<UserSearch
								value={selectedPersonName}
								onSelect={handleUserSelect}
								onClear={handleClearUser}
								onAddUser={handleAddUser}
								isEditMode={editingResult != null}
								userSelected={selectedPersonId != null}
								bind:searchTerm={userInputRawValue}
							/>
						</div>

						<ResultForm bind:formData {editingResult} {submitting} onSubmit={submitResult} onCancel={resetForm} />
					</div>
				</div>
			</div>
			<div class="lg:col-span-3">
				{#if loading}
					<LoadingScreen message="Loading Competition Data" inline />
				{:else}
					<ResultsTable {competitionResults} onEdit={editResult} onDelete={deleteResult} />
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
