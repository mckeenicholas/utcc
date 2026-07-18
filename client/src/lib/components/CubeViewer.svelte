<script lang="ts">
import "scramble-display";
import type { ClassValue } from "svelte/elements";
import type { WCAEvent } from "$lib/types";

interface Props {
	alg: string;
	eventId: WCAEvent;
	class?: ClassValue;
	width?: string;
	height?: string;
}

const { alg, eventId, class: className = "", width = "auto", height = "auto" }: Props = $props();

const scaleAmount = $derived.by(() => {
	switch (eventId) {
		case "666":
		case "777":
		case "555":
		case "444":
		case "444bf":
		case "555bf":
		case "skewb": {
			return 1.25;
		}
		default: {
			return 1;
		}
	}
});
</script>

<div class={className} style="display: flex; justify-content: center; align-items: center; scale: {scaleAmount}">
	<scramble-display event={eventId} scramble={alg} style="width: {width}; height: {height}"> </scramble-display>
</div>
