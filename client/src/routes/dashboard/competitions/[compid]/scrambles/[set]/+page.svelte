<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import { page } from "$app/state";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import ScrambleViewer from "$lib/components/ScrambleViewer.svelte";
import authFetch from "$lib/authFetch";
import { type ScrambleResponse, eventNames } from "$lib/types";
import { BASE_URL } from "$lib/utils";

let scrambles: string[] = $state([]);
let extraScrambles: string[] = $state([]);
let compData: ScrambleResponse | null = $state(null);
let loading = $state(true);

const { compid, set } = page.params;

const fetchScrambles = async () => {
	const scrambleResponse = await authFetch(`${BASE_URL}/api/scrambles/${compid}/${set}/`);

	if (scrambleResponse.status === 403) {
		goto("/dashboard/signin");
	}

	const competitionData: ScrambleResponse = await scrambleResponse.json();

	if (!competitionData) {
		return;
	}

	scrambles = competitionData.scrambles
		.filter((scramble) => scramble.scramble_num > 0)
		.toSorted((a, b) => a.scramble_num - b.scramble_num)
		.map((scramble) => scramble.scramble);

	extraScrambles = competitionData.scrambles
		.filter((scramble) => scramble.scramble_num < 0)
		.toSorted((a, b) => a.scramble_num - b.scramble_num)
		.map((scramble) => scramble.scramble);

	compData = competitionData;

	loading = false;
};

onMount(fetchScrambles);
</script>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-4xl px-4 sm:px-6">
		{#if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen message="Loading Scrambles..." inline minHeight="15rem" />
			</div>
		{:else if compData}
			<div class="mb-6 flex flex-col gap-2">
				<a
					href="/dashboard/competitions/{compid}/scrambles"
					class="text-xs font-semibold text-uoft-blue transition-colors hover:text-uoft-blue-80"
				>
					&larr; Back to Scramble Sets
				</a>
				<h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">
					{compData.competition}: {eventNames[compData.event]} Round {compData.round}
				</h1>
			</div>

			<div class="flex items-center justify-center">
				<ScrambleViewer event={compData.event} {scrambles} extras={extraScrambles} />
			</div>
		{/if}
	</div>
</div>
