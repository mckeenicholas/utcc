<script lang="ts">
import { goto } from "$app/navigation";
import { page } from "$app/state";
import authFetch from "$lib/authFetch";
import Backbutton from "$lib/components/Backbutton.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import ScrambleViewer from "$lib/components/ScrambleViewer.svelte";
import { eventNames, type ScrambleResponse } from "$lib/types";
import { BASE_URL } from "$lib/utils";
import { onMount } from "svelte";

let scrambles: string[] = $state([]);
let extraScrambles: string[] = $state([]);
let compData: ScrambleResponse | null = $state(null);
let loading = $state(true);

const { compid, set } = page.params;

const fetchScrambles = async () => {
	const scrambleResponse = await authFetch(`${BASE_URL}/api/scrambles/${compid}/${set}/`);

	if (scrambleResponse.status == 403) {
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

<Backbutton />
<div class="-mt-4">
	{#if loading}
		<LoadingScreen message="Loading Scrambles" />
	{:else if compData}
		<p class="mb-2 text-center text-2xl font-bold">
			Scrambles for {compData.competition} - {eventNames[compData.event]} Round {compData.round}
		</p>
		<div class="m-4 mb-8 flex items-center justify-center">
			<ScrambleViewer event={compData.event} {scrambles} extras={extraScrambles} />
		</div>
	{/if}
</div>
