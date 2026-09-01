<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import { page } from "$app/state";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import ScrambleCard from "$lib/components/ScrambleCard.svelte";
import SelectMenu from "$lib/components/SelectMenu.svelte";
import authFetch from "$lib/authFetch";
import { eventNames, eventListIdx, eventSolves, type CompetitionScrambleSets, type WCAEvent } from "$lib/types";
import { BASE_URL } from "$lib/utils";

const eventOptions = Object.entries(eventNames)
	.map(([key, name]) => ({
		label: name,
		value: key,
	}))
	.toSorted((a, b) => eventListIdx[a.value as WCAEvent] - eventListIdx[b.value as WCAEvent]);

const compId = page.params.compid;

let competitionScrambles: CompetitionScrambleSets | null = $state(null);
let selectedEvent: WCAEvent = $state("333");
let selectedRound = $state(1);
let selectedCount = $state(1);
let loading = $state(true);
let generating = $state(false);

const fetchScrambles = async () => {
	const response = await authFetch(`${BASE_URL}/api/competitions/${compId}/scrambles/`);

	if (response.status === 403) {
		goto("/dashboard/signin");
	}

	competitionScrambles = await response.json();
	loading = false;
};

onMount(fetchScrambles);

const generateScrambleSet = async () => {
	if (selectedEvent === "333mbf") {
		console.error("333 Multi-Blind scrambles are not implemented yet");
		return;
	}

	generating = true;

	const numScrambles = eventSolves[selectedEvent]! + 2;

	await authFetch(`${BASE_URL}/api/scrambles/${compId}/${selectedEvent}/${selectedRound}/generate/`, {
		body: JSON.stringify({
			count: numScrambles,
			numSets: selectedCount,
		}),
		headers: {
			"Content-Type": "application/json",
		},
		method: "POST",
	});

	await fetchScrambles();

	generating = false;
};

const deleteScramble = async (setId: number) => {
	const response = await authFetch(`${BASE_URL}/api/scrambles/${compId}/${setId}/`, {
		method: "DELETE",
	});

	if (!response.ok) {
		console.error(response.statusText);
	}

	await fetchScrambles();
};

const updateVisibility = async (setId: number, visibility: boolean) => {
	const response = await authFetch(`${BASE_URL}/api/scrambles/${compId}/${setId}/visibility/`, {
		body: JSON.stringify({ visibility }),
		headers: { "Content-Type": "application/json" },
		method: "PATCH",
	});

	if (!response.ok) {
		console.error(response.statusText);
	}

	await fetchScrambles();
};
</script>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-4xl px-4 sm:px-6">
		<div class="mb-6 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
			<div>
				<a
					href="/dashboard/competitions"
					class="text-xs font-semibold text-uoft-blue transition-colors hover:text-uoft-blue-80"
				>
					&larr; Back to Competitions
				</a>
				<h1 class="mt-2 text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Manage Scrambles</h1>
			</div>
		</div>

		{#if generating}
			<div class="mb-6 rounded-sm border border-uoft-blue/20 bg-uoft-blue/5 p-4">
				<div class="flex items-center">
					<div class="me-4 h-5 w-5 animate-spin rounded-full border-2 border-gray-200 border-t-uoft-blue"></div>
					<p class="text-xs font-semibold text-uoft-blue">Generating scrambles...</p>
				</div>
			</div>
		{/if}

		<!-- Generate Scrambles Section -->
		<div class="mb-6 border border-gray-200 bg-white p-6">
			<h2 class="mb-4 text-base font-bold text-gray-900">Generate New Scramble Set</h2>
			<div class="space-y-4">
				<div>
					<label for="event" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase">Event</label>
					<div class="mt-1">
						<SelectMenu bind:value={selectedEvent} options={eventOptions} />
					</div>
				</div>

				<div class="flex gap-3">
					<div class="w-full">
						<label for="round" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase">Round</label>
						<input
							bind:value={selectedRound}
							id="round"
							type="number"
							min="1"
							class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-xs text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
						/>
					</div>
					<div class="w-full">
						<label for="count" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase">Count</label>
						<input
							bind:value={selectedCount}
							id="count"
							type="number"
							min="1"
							class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-xs text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
						/>
					</div>
				</div>

				<button
					onclick={generateScrambleSet}
					disabled={!selectedEvent || generating}
					class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 disabled:opacity-50"
				>
					{generating ? "Generating..." : "Generate Scramble Set"}
				</button>
			</div>
		</div>

		<!-- Existing Scrambles Section -->
		{#if loading}
			<LoadingScreen message="Loading Scrambles" inline />
		{:else}
			<div class="mt-4 mb-8">
				<div class="mb-4">
					<h2 class="text-lg font-bold text-gray-900">Available Scramble Sets</h2>
				</div>

				{#if competitionScrambles && competitionScrambles.length > 0}
					{#each competitionScrambles as eventData (eventData.event)}
						<div class="mb-4 divide-y divide-gray-100 border border-gray-200 bg-white">
							{#each eventData.rounds as roundData (roundData.round)}
								<div class="flex items-center space-x-4 bg-gray-50/50 p-2.5 ps-4">
									<div class="min-w-0 text-xs font-bold text-gray-900">
										{eventNames[eventData.event]}
									</div>
									<div class="text-xs text-gray-700">
										Round {roundData.round}
									</div>
								</div>
								{#each roundData.sets as scrambleSet (scrambleSet.id)}
									<div class="px-4">
										<ScrambleCard
											compId={compId!}
											scrambleSetId={scrambleSet.id}
											setNum={scrambleSet.scramble_set}
											visibility={scrambleSet.visible}
											onDelete={() => deleteScramble(scrambleSet.id)}
											onSetVisibility={(status) => updateVisibility(scrambleSet.id, status)}
										/>
									</div>
								{/each}
							{/each}
						</div>
					{/each}
				{:else}
					<div class="border border-gray-200 bg-white p-8 text-center">
						<p class="text-xs text-gray-700">No scramble sets found for this competition.</p>
					</div>
				{/if}
			</div>
		{/if}
	</div>
</div>
