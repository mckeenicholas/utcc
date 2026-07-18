<script lang="ts">
import type { User } from "$lib/types";

interface Props {
	user: User;
	ondelete: (id: number) => void;
	onsave: (id: number, name: string, studentStatus: string) => void;
}

const { user, ondelete, onsave }: Props = $props();

let isEditing = $state(false);
let editUserName = $state("");
let editUserStudentStatus = $state("UTSG");

const startEdit = () => {
	editUserName = user.name;
	editUserStudentStatus = user.student_designator;
	isEditing = true;
};

const cancelEdit = () => {
	isEditing = false;
};

const handleSave = () => {
	if (editUserName.trim()) {
		onsave(user.id, editUserName, editUserStudentStatus);
		isEditing = false;
	}
};
</script>

<div class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md">
	<div class="flex items-center justify-between">
		<div class="mr-4 flex-1">
			<div class="flex items-center space-x-3">
				<div
					class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-100 text-lg font-medium text-blue-600"
				>
					{user.name.charAt(0).toUpperCase()}
				</div>
				<div class="min-w-0 flex-1">
					{#if isEditing}
						<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
							<input
								bind:value={editUserName}
								onkeydown={(e) => e.key === "Enter" && handleSave()}
								class="rounded-md border border-gray-300 px-2 py-1 text-sm font-medium text-gray-900 focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
							/>
							<select
								bind:value={editUserStudentStatus}
								class="rounded-md border border-gray-300 bg-white px-2 py-1 text-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
							>
								<option value="UTSG">UTSG</option>
								<option value="UTM">UTM</option>
								<option value="UTSC">UTSC</option>
								<option value="Non-UofT">Non-UofT</option>
							</select>
						</div>
					{:else}
						<p class="truncate text-sm font-medium text-gray-900">
							{user.name}
							<span
								class="ml-1 rounded border border-blue-100 bg-blue-50 px-2 py-0.5 text-xs font-semibold text-blue-700"
							>
								{user.student_designator}
							</span>
						</p>
					{/if}
					<p class="mt-1 text-xs text-gray-500">ID: {user.id}</p>
				</div>
			</div>
		</div>
		<div class="flex shrink-0 space-x-2">
			{#if isEditing}
				<button
					onclick={handleSave}
					disabled={!editUserName.trim()}
					class="rounded-md bg-green-100 px-3 py-1 text-sm text-green-800 hover:bg-green-200 disabled:cursor-not-allowed! disabled:bg-gray-100 disabled:text-gray-800 disabled:hover:bg-gray-200"
				>
					Save
				</button>
				<button onclick={cancelEdit} class="rounded-md bg-gray-100 px-3 py-1 text-sm text-gray-800 hover:bg-gray-200">
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
					onclick={() => ondelete(user.id)}
					class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>
