<script lang="ts">
import { WCAEventList, type WCAEvent } from '$lib/types';
import { sortEvents } from '$lib/utils';
import CubeIcon from './CubeIcon.svelte';

interface Props {
	selectedEvent: WCAEvent;
	events?: WCAEvent[];
}

let { selectedEvent = $bindable(), events }: Props = $props();

const eventList = $derived(events ?? WCAEventList.sort(sortEvents));
</script>

<div class="flex flex-wrap space-x-1 rounded-md border border-gray-200 p-0.5">
	{#each eventList as eventId (eventId)}
		<button onclick={() => (selectedEvent = eventId)}>
			<CubeIcon
				event={eventId}
				class="{selectedEvent == eventId ? 'bg-gray-300' : 'bg-clear'}  cursor-pointer rounded-md px-2.5 py-1 "
			/>
		</button>
	{/each}
</div>
