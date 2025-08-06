<script lang="ts">
import { page } from '$app/stores';
import Backbutton from '$lib/components/Backbutton.svelte';
import EventPicker from '$lib/components/EventPicker.svelte';
import LoadingScreen from '$lib/components/LoadingScreen.svelte';
import {
	eventListIdx,
	eventNames,
	eventSolves,
	type ProfileRecordDetail,
	type ProfileResponse,
	type WCAEvent
} from '$lib/types';
import { BASE_URL, getMeanType, renderTime } from '$lib/utils';
import { onMount } from 'svelte';

let personResults: ProfileResponse | null = $state(null);
let selectedEvent: WCAEvent = $state('333');
let loading = $state(true);
let error = $state(false);

onMount(async () => {
	try {
		const response = await fetch(`${BASE_URL}/api/users/${$page.params.id}/results/`);
		if (!response.ok) {
			error = true;
			return;
		}
		personResults = await response.json();
	} catch (err) {
		console.error('Failed to fetch person results:', err);
		error = true;
	} finally {
		loading = false;
	}
});

const recordDisplayObj = $derived.by(() => {
	if (!personResults) {
		return [];
	}

	const recordEntries = Object.entries(personResults.records);
	recordEntries.sort((a, b) => {
		const eventA = a[0] as WCAEvent;
		const eventB = b[0] as WCAEvent;
		return eventListIdx[eventA] - eventListIdx[eventB];
	}) as [WCAEvent, ProfileRecordDetail][];

	return recordEntries;
});

const shownResults = $derived.by(() => {
	if (!personResults) {
		return null;
	}

	const eventResult = personResults.results.find((event) => event.event == selectedEvent);
	if (!eventResult) return null;

	const sortedEventResult = {
		...eventResult,
		competitions: eventResult.competitions
			.map((comp) => ({
				...comp,
				rounds: [...comp.rounds].sort((a, b) => a.round - b.round)
			}))
			.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
	};

	return sortedEventResult;
});

const personalRecords = $derived.by(() => {
	if (!shownResults) return new Set<string>();

	const allResults = shownResults.competitions
		.flatMap((comp) =>
			comp.rounds.map((round) => ({
				single: round.single,
				average: round.average,
				date: comp.date,
				competitionId: comp.id,
				round: round.round
			}))
		)
		.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

	const records = allResults.reduce(
		(acc, result) => {
			const { bestSingle, bestAverage, records } = acc;

			// Check for new personal single record
			if (result.single > 0 && (bestSingle === 0 || result.single < bestSingle)) {
				acc.bestSingle = result.single;
				records.add(`single-${result.competitionId}-${result.round}`);
			}

			// Check for new personal average record
			if (result.average > 0 && (bestAverage === 0 || result.average < bestAverage)) {
				acc.bestAverage = result.average;
				records.add(`average-${result.competitionId}-${result.round}`);
			}

			return acc;
		},
		{ bestSingle: 0, bestAverage: 0, records: new Set<string>() }
	).records;

	return records;
});
</script>

<Backbutton />
{#if loading}
	<LoadingScreen message="Loading Profile" inline={true} minHeight="30rem" />
{:else if error}
	<div class="bg-gray-50 py-8">
		<div class="mx-auto max-w-6xl px-4">
			<div class="rounded-lg bg-white p-8 text-center shadow-sm">
				<h3 class="text-lg font-medium text-gray-900">Person Not Found</h3>
				<p class="mt-2 text-gray-600">The requested person could not be found.</p>
			</div>
		</div>
	</div>
{:else if personResults}
	<div class=" bg-gray-50 py-8">
		<div class="mx-auto max-w-6xl px-4">
			<!-- Header -->
			<div class="mb-8">
				<h1 class="text-3xl font-bold text-gray-900">{personResults.person.name}</h1>
				<p class="mt-2 text-gray-600">Competition Profile</p>
			</div>

			<!-- Personal Records -->
			<div class="mb-8 overflow-hidden rounded-lg bg-white shadow-sm">
				<div class="border-b border-gray-200 px-6 py-4">
					<h2 class="text-xl font-semibold text-gray-800">Personal Records</h2>
				</div>
				<div class="overflow-x-auto">
					<table class="min-w-full divide-y divide-gray-200">
						<thead class="bg-gray-50">
							<tr>
								<th
									class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
									>Event</th
								>
								<th
									class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
									>Single</th
								>
								<th
									class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
									>Average</th
								>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-200 bg-white">
							{#each recordDisplayObj as [eventName, data] (eventName)}
								<tr class="transition-colors duration-100 ease-in-out hover:bg-gray-100">
									<td class="px-6 py-4 text-sm font-medium whitespace-nowrap text-gray-900">
										{eventNames[eventName as WCAEvent]}
									</td>
									<td
										class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap text-gray-900"
									>
										{renderTime(data.single)}
									</td>
									<td
										class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap text-gray-900"
									>
										{renderTime(data.average)}
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			</div>

			<!-- Competition Results -->
			<div class="overflow-hidden rounded-lg bg-white shadow-sm">
				<div class="my-4 flex justify-center">
					<EventPicker bind:selectedEvent={selectedEvent} />
				</div>
				{#if shownResults}
					<div class="border-b border-gray-200 px-6 pb-4">
						<h2 class="text-xl font-semibold text-gray-800">
							Results for {eventNames[selectedEvent]}
						</h2>
					</div>
					<div class="overflow-x-auto">
						<table class="min-w-full divide-y divide-gray-200">
							<thead class="bg-gray-50">
								<tr>
									<th
										class="px-6 py-3 text-left text-xs font-medium tracking-wider text-gray-500 uppercase"
										>Competition</th
									>
									<th
										class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
										>Round</th
									>
									<th
										class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
										>Single</th
									>
									<th
										class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
									>
										{getMeanType(selectedEvent)}
									</th>
									{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
										<th
											class="px-6 py-3 text-center text-xs font-medium tracking-wider text-gray-500 uppercase"
										>
											Solve {idx + 1}
										</th>
									{/each}
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-200 bg-white">
								{#each shownResults.competitions as competition (competition.id)}
									{#each competition.rounds as round, roundIndex (round.round)}
										<tr class="transition-colors duration-100 ease-in-out hover:bg-gray-100">
											<td class="px-6 py-4 text-sm whitespace-nowrap text-gray-900">
												{#if roundIndex == 0}
													<a href="/competitions/{competition.id}" class="hover:text-gray-400">
														{competition.name}
													</a>
												{/if}
											</td>
											<td class="px-6 py-4 text-center text-sm whitespace-nowrap text-gray-900">
												{round.round}
											</td>
											<td
												class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap"
												class:text-blue-600={personalRecords.has(`single-${competition.id}-${round.round}`)}
												class:text-gray-900={!personalRecords.has(`single-${competition.id}-${round.round}`)}
											>
												{renderTime(round.single)}
											</td>
											<td
												class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap"
												class:text-blue-600={personalRecords.has(`average-${competition.id}-${round.round}`)}
												class:text-gray-900={!personalRecords.has(`average-${competition.id}-${round.round}`)}
											>
												{renderTime(round.average)}
											</td>
											{#each Array.from({ length: eventSolves[selectedEvent]! }).keys() as idx (idx)}
												<td
													class="px-6 py-4 text-center font-mono text-sm whitespace-nowrap text-gray-700"
												>
													{renderTime(round.times[idx])}
												</td>
											{/each}
										</tr>
									{/each}
								{/each}
							</tbody>
						</table>
					</div>
				{:else}
					<div class="rounded-lg bg-white p-8 text-center shadow-sm">
						<h3 class="text-lg font-medium text-gray-900">
							No results for {eventNames[selectedEvent]}
						</h3>
						<p class="mt-2 text-gray-600">This person hasn't competed in this event yet.</p>
					</div>
				{/if}
			</div>
		</div>
	</div>
{/if}
