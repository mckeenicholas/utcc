<script lang="ts">
import { page } from '$app/state';
import authFetch from '$lib/authFetch';
import { generateScrambles } from '$lib/scrambleService';
import { eventListIdx, eventSolves, type CompetitionScrambleSets, type WCAEvent } from '$lib/types';
import { BASE_URL } from '$lib/utils';
import { onMount } from 'svelte';
import { Select } from 'bits-ui';
import { eventNames } from '$lib/types';
import Backbutton from '$lib/components/Backbutton.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import ScrambleCard from '$lib/components/ScrambleCard.svelte';
import { goto } from '$app/navigation';

const eventOptions = Object.entries(eventNames)
	.map(([key, name]) => ({
		value: key,
		label: name
	}))
	.sort((a, b) => eventListIdx[a.value as WCAEvent] - eventListIdx[b.value as WCAEvent]);

const scrambleIds = [-1, -2, 1, 2, 3, 4, 5];

const compId = page.params.compid;

let competitionScrambles: CompetitionScrambleSets | null = $state(null);
let selectedEvent: WCAEvent = $state('333');
let selectedRound = $state(1);
let selectedCount = $state(1);
let loading = $state(true);
let generating = $state(false);

const fetchScrambles = async () => {
	const response = await authFetch(`${BASE_URL}/api/competitions/${compId}/scrambles/`);

	if (response.status == 403) {
		goto('/dashboard/signin');
	}

	competitionScrambles = await response.json();
	loading = false;
};

onMount(fetchScrambles);

const generateScrambleSet = async () => {
	if (selectedEvent == '333mbf') {
		console.log('333 Multi-Blind scrambles are not implemented yet');
		return;
	}

	generating = true;

	const numScrambles = eventSolves[selectedEvent]! + 2;

	await Promise.all(
		Array.from({ length: selectedCount }).map(() => generateAndSubmit(numScrambles))
	);

	await fetchScrambles();

	generating = false;
};

const generateAndSubmit = async (numScrambles: number) => {
	const scrambles = await generateScrambles(selectedEvent, numScrambles);

	const scrambleObjs = scrambles.map((scramble, idx) => ({
		scramble,
		scramble_num: scrambleIds[idx]
	}));

	await authFetch(`${BASE_URL}/api/scrambles/${compId}/${selectedEvent}/${selectedRound}/`, {
		method: 'POST',
		body: JSON.stringify(scrambleObjs),
		headers: {
			'Content-Type': 'application/json'
		}
	});
};

const deleteScramble = async (setId: number) => {
	const response = await authFetch(`${BASE_URL}/api/scrambles/${compId}/${setId}/`, {
		method: 'DELETE'
	});

	if (!response.ok) {
		console.error(response.statusText);
	}

	await fetchScrambles();
};

const updateVisibility = async (setId: number, visibility: boolean) => {
	const response = await authFetch(`${BASE_URL}/api/scrambles/${compId}/${setId}/visibility/`, {
		method: 'PATCH',
		body: JSON.stringify({ visibility }),
		headers: { 'Content-Type': 'application/json' }
	});

	if (!response.ok) {
		console.error(response.statusText);
	}

	await fetchScrambles();
};
</script>

<Backbutton />
<div class="min-h-screen pb-8">
	<div class="mx-auto max-w-4xl px-4">
		{#if generating}
			<div class="mb-6 rounded-lg border border-blue-200 bg-blue-50 p-4">
				<div class="flex items-center">
					<div
						class="me-4 h-6 w-6 animate-spin rounded-full border-2 border-blue-200 border-t-blue-600"
					></div>
					<p class="font-medium text-blue-700">
						Generating scrambles. Please do not refresh this page.
					</p>
				</div>
			</div>
		{/if}

		<!-- Generate Scrambles Section -->
		<div class="mb-8 rounded-lg bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-semibold text-gray-800">Generate New Scramble Set</h2>
			<div class="space-y-4">
				<div>
					<label for="event" class="block text-sm font-medium text-gray-700">Event</label>
					<Select.Root items={eventOptions} bind:value={selectedEvent} type="single">
						<Select.Trigger
							class="mt-1 flex w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-left shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
							aria-label="Select an event"
						>
							<span>
								{eventOptions.find((option) => option.value === selectedEvent)?.label ||
									'Select Event'}
							</span>
							<svg
								class="ml-2 h-4 w-4 shrink-0 text-gray-400"
								fill="none"
								stroke="currentColor"
								viewBox="0 0 24 24"
							>
								<path
									stroke-linecap="round"
									stroke-linejoin="round"
									stroke-width="2"
									d="M19 9l-7 7-7-7"
								/>
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
													<span
														class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center"
													>
														<svg
															class="h-4 w-4"
															fill="none"
															stroke="currentColor"
															viewBox="0 0 24 24"
														>
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

				<div class="flex">
					<div class="w-full">
						<label for="round" class="block text-sm font-medium text-gray-700">Round</label>
						<input
							bind:value={selectedRound}
							id="round"
							type="number"
							min="1"
							class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
						/>
					</div>
					<div class="ms-4 w-full">
						<label for="count" class="block text-sm font-medium text-gray-700">Count</label>
						<input
							bind:value={selectedCount}
							id="count"
							type="number"
							min="1"
							class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
						/>
					</div>
				</div>

				<button
					onclick={generateScrambleSet}
					disabled={!selectedEvent || generating}
					class="w-full rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-400"
				>
					{generating ? 'Generating...' : 'Generate Scramble Set'}
				</button>
			</div>
		</div>

		<!-- Existing Scrambles Section -->
		{#if loading}
			<LoadingScreen message="Loading Scrambles" inline />
		{:else}
			<div class="mt-4 mb-8">
				<div class="mb-4">
					<h2 class="ms-2 text-2xl font-semibold text-gray-800">Available Scramble Sets</h2>
				</div>

				{#if competitionScrambles && competitionScrambles.length > 0}
					{#each competitionScrambles as eventData (eventData.event)}
						<div
							class="mb-4 divide-y divide-gray-200 overflow-hidden rounded-lg bg-white shadow-sm"
						>
							{#each eventData.rounds as roundData (roundData.round)}
								<div class="flex items-center space-x-4 p-2 ps-4">
									<div class="min-w-0 font-semibold text-gray-900">
										{eventNames[eventData.event]}
									</div>
									<div class="text-sm text-gray-500">
										Round {roundData.round}
									</div>
								</div>
								{#each roundData.sets as scrambleSet (scrambleSet.id)}
									<ScrambleCard
										compId={compId!}
										scrambleSetId={scrambleSet.id}
										setNum={scrambleSet.scramble_set}
										visibility={scrambleSet.visible}
										onDelete={() => deleteScramble(scrambleSet.id)}
										onSetVisibility={(status) => updateVisibility(scrambleSet.id, status)}
									/>
								{/each}
							{/each}
						</div>
					{/each}
				{:else}
					<div class="rounded-lg bg-white p-6 shadow-sm">
						<p class="text-center text-gray-500">No scramble sets found for this competition.</p>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
