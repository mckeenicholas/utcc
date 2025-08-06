<script lang="ts">
import { eventNames, type WCAEvent } from '$lib/types';
import CubeIcon from './CubeIcon.svelte';

interface Props {
	selectedEvent: WCAEvent;
}

let { selectedEvent = $bindable() }: Props = $props();
</script>

<div class="flex flex-wrap space-x-1 rounded-md border border-gray-200 p-0.5">
	{#each Object.keys(eventNames) as eventIdStr (eventIdStr)}
		{@const eventId = eventIdStr as WCAEvent}
		<button onclick={() => (selectedEvent = eventId)}>
			<CubeIcon
				event={eventId}
				class="{selectedEvent == eventId ? 'bg-gray-300' : 'bg-clear'}  cursor-pointer rounded-md px-2.5 py-1 "
			/>
		</button>
	{/each}
</div>
