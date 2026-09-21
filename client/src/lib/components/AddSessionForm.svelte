<script lang="ts">
import DateForm from "./DateForm.svelte";

interface Props {
	onAddSession: (name: string, date: string) => Promise<void>;
}
const { onAddSession }: Props = $props();

let newSessionName = $state("");
let startDate = $state<string>(new Date().toISOString().split("T")[0]);

const handleSubmit = async () => {
	if (newSessionName.trim()) {
		await onAddSession(newSessionName.trim(), startDate);
		newSessionName = "";
	}
};
</script>

<div class="mb-6 border border-border bg-surface p-6">
	<h2 class="mb-4 text-base font-bold text-main">Add New Session</h2>
	<div class="space-y-4">
		<div>
			<label for="new-session-name" class="block text-xs font-semibold tracking-wider text-secondary uppercase"
				>Session Name</label
			>
			<input
				id="new-session-name"
				placeholder="Enter session name (e.g., 2025 Fall)"
				bind:value={newSessionName}
				onkeydown={(e) => e.key === "Enter" && handleSubmit()}
				class="mt-1 block w-full rounded-sm border border-border-strong bg-surface px-3 py-1.5 text-sm text-main placeholder:text-muted focus:border-brand focus:ring-1 focus:ring-brand focus:outline-none"
			/>
		</div>
		<div>
			<DateForm bind:selectedDate={startDate} label="Session start date (used for ordering)" />
		</div>
		<button
			onclick={handleSubmit}
			disabled={!newSessionName.trim()}
			class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 disabled:opacity-50 dark:border dark:border-blue-500/30 dark:hover:bg-blue-900"
		>
			Add Session
		</button>
	</div>
</div>
