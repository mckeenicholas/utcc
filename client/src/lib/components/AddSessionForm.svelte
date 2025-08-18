<script lang="ts">
interface Props {
	onAddSession: (name: string) => Promise<void>;
}
let { onAddSession }: Props = $props();

let newSessionName = $state('');

const handleSubmit = async () => {
	if (newSessionName.trim()) {
		await onAddSession(newSessionName.trim());
		newSessionName = '';
	}
};
</script>

<div class="mb-8 rounded-lg bg-white p-6 shadow-sm">
	<h2 class="mb-4 text-xl font-semibold text-gray-800">Add New Session</h2>
	<div class="space-y-4">
		<div>
			<label for="new-session-name" class="block text-sm font-medium text-gray-700"
				>Session Name</label
			>
			<input
				id="new-session-name"
				placeholder="Enter session name (e.g., 2025 Fall)"
				bind:value={newSessionName}
				onkeydown={(e) => e.key === 'Enter' && handleSubmit()}
				class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
			/>
		</div>
		<button
			onclick={handleSubmit}
			disabled={!newSessionName.trim()}
			class="w-full rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-400"
		>
			Add Session
		</button>
	</div>
</div>
