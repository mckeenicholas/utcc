<script lang="ts">
import { type Session, type WCAEvent } from '$lib/types';
import { onMount } from 'svelte';
import EventPicker from './EventPicker.svelte';
import SessionSelector from './SessionSelector.svelte';
import ToggleButton from './ToggleButton.svelte';
import { fetchSessions } from '$lib/competitionSessionService';
import Switch from './Switch.svelte';

interface Props {
	isAverage: boolean;
	selectedEvent: WCAEvent;
	showAll: boolean;
	session: string;
	isStudent: boolean;
}

let {
	isAverage = $bindable(),
	selectedEvent = $bindable(),
	showAll = $bindable(),
	session = $bindable(),
	isStudent = $bindable()
}: Props = $props();

let sessions: Session[] = $state([]);

onMount(async () => {
	sessions = await fetchSessions();
});
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
	<div class="flex gap-4">
		<SessionSelector bind:value={session} sessionData={sessions} class="mt-2" />
		<div class="flex flex-col items-center justify-center">
			<Switch label="Show UofT Students Only" bind:checked={isStudent} class="mt-2" />
		</div>
	</div>
</div>
