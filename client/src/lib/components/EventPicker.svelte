<script lang="ts">
import { type WCAEvent, WCAEventList, eventNames } from "$lib/types";
import { sortEvents } from "$lib/utils";
import CubeIcon from "./CubeIcon.svelte";

interface Props {
	selectedEvent: WCAEvent;
	events?: WCAEvent[];
}

let { selectedEvent = $bindable(), events }: Props = $props();

const eventList = $derived(events ?? WCAEventList.toSorted(sortEvents));
</script>

<div class="inline-flex flex-wrap items-center gap-1 rounded-sm border border-border bg-surface p-1">
	{#each eventList as eventId (eventId)}
		<button
			type="button"
			onclick={() => (selectedEvent = eventId)}
			class="inline-flex cursor-pointer items-center justify-center rounded-sm p-2 text-sm transition-colors focus:outline-none {selectedEvent ===
			eventId
				? 'bg-uoft-blue text-white dark:border dark:border-blue-500/30'
				: 'text-secondary hover:bg-surface-muted hover:text-main'}"
			aria-label="Select {eventNames[eventId] ?? eventId}"
		>
			<CubeIcon event={eventId} />
		</button>
	{/each}
</div>
