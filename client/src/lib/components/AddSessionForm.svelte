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

<div class="mb-6 border border-gray-200 bg-white p-6">
	<h2 class="mb-4 text-base font-bold text-gray-900">Add New Session</h2>
	<div class="space-y-4">
		<div>
			<label for="new-session-name" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase"
				>Session Name</label
			>
			<input
				id="new-session-name"
				placeholder="Enter session name (e.g., 2025 Fall)"
				bind:value={newSessionName}
				onkeydown={(e) => e.key === "Enter" && handleSubmit()}
				class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
			/>
		</div>
		<div>
			<DateForm bind:selectedDate={startDate} label="Session start date (used for ordering)" />
		</div>
		<button
			onclick={handleSubmit}
			disabled={!newSessionName.trim()}
			class="w-full rounded-sm bg-uoft-blue px-4 py-2 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 disabled:opacity-50"
		>
			Add Session
		</button>
	</div>
</div>
