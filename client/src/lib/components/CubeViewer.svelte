<script lang="ts">
import 'cubing/twisty';
import type { WCAEvent } from '$lib/types';
import { Alg } from 'cubing/alg';
import { eventInfo } from 'cubing/puzzles';
import type { ClassValue } from 'svelte/elements';

interface Props {
	alg: Alg | string;
	eventId: WCAEvent;
	class?: ClassValue;
	width?: string;
	height?: string;
}

let { alg, eventId, class: className = '', width = 'auto', height = 'auto' }: Props = $props();

let algObj = $derived(typeof alg === 'string' ? new Alg(alg) : alg);

let scaleAmount = $derived.by(() => {
	switch (eventId) {
		case '666':
		case '777':
		case '555':
		case '444':
		case '444bf':
		case '555bf':
		case 'skewb':
			return 1.25;
		default:
			return 1;
	}
});
</script>

<div
	class={className}
	style="display: flex; justify-content: center; align-items: center; scale: {scaleAmount}"
>
	<twisty-player
		visualization="2D"
		background="none"
		control-panel="none"
		puzzle={eventInfo(eventId)!.puzzleID}
		alg={algObj}
		style="width: {width}; height: {height}"
	>
	</twisty-player>
</div>
