<script lang="ts">
import { WCAEventList, type WCAEvent } from '$lib/types';
import CubeIcon from './CubeIcon.svelte';

interface Props {
	selectedEvent: WCAEvent;
	events?: WCAEvent[];
}

let { selectedEvent = $bindable(), events = WCAEventList }: Props = $props();
</script>

<div class="flex flex-wrap space-x-1 rounded-md border border-gray-200 p-0.5">
	{#each events as eventId (eventId)}
		<button onclick={() => (selectedEvent = eventId)}>
			<CubeIcon
				event={eventId}
				class="{selectedEvent == eventId ? 'bg-gray-300' : 'bg-clear'}  cursor-pointer rounded-md px-2.5 py-1 "
			/>
		</button>
	{/each}
</div>
