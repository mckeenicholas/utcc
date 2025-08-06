<script lang="ts">
import type { WCAEvent } from '$lib/types';
import EventPicker from './EventPicker.svelte';

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
	<div class="flex flex-col gap-2 lg:flex-row lg:flex-wrap lg:items-center lg:justify-between">
		<!-- Event selector -->
		<EventPicker bind:selectedEvent={selectedEvent} />

		<!-- Toggle buttons -->
		<div class="flex flex-wrap gap-2">
			<ToggleButton bind:value={isAverage} leftLabel="Single" rightLabel="Average" />
			<ToggleButton bind:value={showAll} leftLabel="Persons" rightLabel="Results" />
		</div>
	</div>
</div>
