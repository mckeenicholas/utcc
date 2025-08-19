<script lang="ts">
import type { Session } from '$lib/types';

interface Props {
	session: Session;
	onDelete: (id: number) => void;
	onSave: (id: number, name: string, date: string) => void;
}

let { session, onDelete, onSave }: Props = $props();

let isEditing = $state(false);
let editSessionName = $state(session.name);
let editSessionDate = $state(session.start_date);

const startEdit = () => {
	isEditing = true;
};

const cancelEdit = () => {
	isEditing = false;
};

const handleSave = () => {
	if (editSessionName.trim()) {
		onSave(session.id, editSessionName.trim(), editSessionDate);
		isEditing = false;
	} else {
		isEditing = false;
	}
};
</script>

<div
	class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
>
	<div class="flex items-center justify-between">
		<div class="flex items-center space-x-3">
			<div
				class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-lg font-medium text-blue-600"
			>
				{session.name.charAt(0).toUpperCase()}
			</div>
			<div>
				{#if isEditing}
					<input
						bind:value={editSessionName}
						onkeydown={(e) => e.key === 'Enter' && handleSave()}
						class="rounded-md border border-gray-300 px-2 py-1 text-sm font-medium text-gray-900 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
					/>
					<input type="date" bind:value={editSessionDate} class="ms-2" />
				{:else}
					<span class="text-sm font-medium text-gray-900">{session.name}</span>
				{/if}
				<p class="text-xs text-gray-500">ID: {session.id} - Start Date: {session.start_date}</p>
			</div>
		</div>
		<div class="flex space-x-2">
			{#if isEditing}
				<button
					onclick={handleSave}
					disabled={!editSessionName.trim()}
					class="rounded-md bg-green-100 px-3 py-1 text-sm text-green-800 hover:bg-green-200 disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-800 disabled:hover:bg-gray-200"
				>
					Save
				</button>
				<button
					onclick={cancelEdit}
					class="rounded-md bg-gray-100 px-3 py-1 text-sm text-gray-800 hover:bg-gray-200"
				>
					Cancel
				</button>
			{:else}
				<button
					onclick={startEdit}
					class="rounded-md bg-yellow-100 px-3 py-1 text-sm text-yellow-800 hover:bg-yellow-200"
				>
					Edit
				</button>
				<button
					onclick={() => onDelete(session.id)}
					class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>
