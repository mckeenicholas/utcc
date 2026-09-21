<script lang="ts">
import { onMount } from "svelte";
import { fetchSessions } from "$lib/competitionSessionService";
import { type Session, type StudentStatus, type WCAEvent } from "$lib/types";
import EventPicker from "./EventPicker.svelte";
import SessionSelector from "./SessionSelector.svelte";
import ToggleButton from "./ToggleButton.svelte";
import UofTSelector from "./UofTSelector.svelte";

interface Props {
	isAverage: boolean;
	selectedEvent: WCAEvent;
	showAll: boolean;
	session: string;
	studentStatus: StudentStatus;
}

let {
	isAverage = $bindable(),
	selectedEvent = $bindable(),
	showAll = $bindable(),
	session = $bindable(),
	studentStatus = $bindable(),
}: Props = $props();

let sessions: Session[] = $state([]);

onMount(async () => {
	sessions = await fetchSessions();
});
</script>

<div class="border border-border bg-surface p-4 sm:p-5">
	<div class="flex flex-wrap items-center gap-4">
		<!-- Event selector -->
		<EventPicker bind:selectedEvent />

		<div class="hidden h-6 w-px bg-border sm:block"></div>

		<!-- Toggle buttons -->
		<div class="flex flex-wrap items-center gap-2">
			<ToggleButton bind:value={isAverage} leftLabel="Single" rightLabel="Average" />
			<ToggleButton bind:value={showAll} leftLabel="Persons" rightLabel="Results" />
		</div>
	</div>
	<div class="mt-4 flex flex-wrap items-center gap-4 border-t border-border pt-4">
		<div class="flex items-center gap-2">
			<span class="text-xs font-medium text-secondary">Session:</span>
			<SessionSelector bind:value={session} sessionData={sessions} />
		</div>
		<div class="flex items-center gap-2">
			<span class="text-xs font-medium text-secondary">Status:</span>
			<UofTSelector bind:status={studentStatus} />
		</div>
	</div>
</div>
