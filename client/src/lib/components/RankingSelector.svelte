<script lang="ts">
	import { eventNames, type WCAEvent } from '$lib/types';
	import CubeIcon from './CubeIcon.svelte';
	import ToggleButton from './ToggleButton.svelte';

	interface Props {
		isAverage: boolean;
		selectedEvent: WCAEvent;
		showAll: boolean;
	}

	let {
		isAverage = $bindable(),
		selectedEvent = $bindable(),
		showAll = $bindable()
	}: Props = $props();
</script>

<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm">
	<div class="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
		<!-- Event selector -->
		<div class="flex flex-wrap space-x-1 rounded-md border p-0.5">
			{#each Object.keys(eventNames) as eventIdStr (eventIdStr)}
				{@const eventId = eventIdStr as WCAEvent}
				<button
					onclick={() => (selectedEvent = eventId)}
					class="{selectedEvent == eventId ? 'bg-gray-300' : 'bg-clear'} rounded-md px-2.5 py-1"
				>
					<CubeIcon event={eventId} class="" />
				</button>
			{/each}
		</div>

		<!-- Toggle buttons -->
		<div class="flex h-[40px] gap-2">
			<ToggleButton bind:value={isAverage} leftLabel="Single" rightLabel="Average" />
			<ToggleButton bind:value={showAll} leftLabel="Persons" rightLabel="Results" />
		</div>
	</div>
</div>
