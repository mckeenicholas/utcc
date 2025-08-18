<script lang="ts">
import { type Session, type WCAEvent } from '$lib/types';
import { onMount } from 'svelte';
import EventPicker from './EventPicker.svelte';
import SessionSelector from './SessionSelector.svelte';
import ToggleButton from './ToggleButton.svelte';
import { fetchSessions } from '$lib/competitionSessionService';

interface Props {
	isAverage: boolean;
	selectedEvent: WCAEvent;
	showAll: boolean;
	session: string;
}

let {
	isAverage = $bindable(),
	selectedEvent = $bindable(),
	showAll = $bindable(),
	session = $bindable()
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
	<SessionSelector bind:value={session} sessionData={sessions} class="mt-2" />
</div>
