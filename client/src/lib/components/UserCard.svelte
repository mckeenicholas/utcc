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

<div class="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-all duration-200 hover:shadow-md">
	<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
		<div class="min-w-0 flex-1">
			<div class="flex items-center space-x-3">
				<div
					class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-blue-100 bg-blue-50 text-lg font-bold text-blue-600"
				>
					{user.name.charAt(0).toUpperCase()}
				</div>
				<div class="min-w-0 flex-1">
					{#if isEditing}
						<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
							<input
								bind:value={editUserName}
								onkeydown={(e) => e.key === "Enter" && handleSave()}
								class="rounded-lg border border-gray-300 px-3 py-1.5 text-sm font-medium text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
							/>
							<select
								bind:value={editUserStudentStatus}
								class="rounded-lg border border-gray-300 bg-white px-3 py-1.5 text-sm font-medium text-gray-900 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
							>
								<option value="UTSG">UTSG</option>
								<option value="UTM">UTM</option>
								<option value="UTSC">UTSC</option>
								<option value="Non-UofT">Non-UofT</option>
							</select>
						</div>
					{:else}
						<p class="flex items-center truncate text-sm font-semibold text-gray-900">
							{user.name}
							<span
								class="ml-2 rounded-md border border-blue-100 bg-blue-50 px-2 py-0.5 text-xs font-bold text-blue-700"
							>
								{user.student_designator}
							</span>
						</p>
					{/if}
					<p class="mt-1 text-xs font-medium text-gray-400">ID: {user.id}</p>
				</div>
			</div>
		</div>
		<div class="flex shrink-0 space-x-2">
			{#if isEditing}
				<button
					onclick={handleSave}
					disabled={!editUserName.trim()}
					class="rounded-lg bg-emerald-50 px-3.5 py-2 text-sm font-semibold text-emerald-700 transition-colors hover:bg-emerald-100 disabled:cursor-not-allowed! disabled:bg-gray-100 disabled:text-gray-400"
				>
					Save
				</button>
				<button
					onclick={cancelEdit}
					class="rounded-lg bg-gray-50 px-3.5 py-2 text-sm font-semibold text-gray-600 transition-colors hover:bg-gray-100"
				>
					Cancel
				</button>
			{:else}
				<button
					onclick={startEdit}
					class="rounded-lg bg-amber-50 px-3.5 py-2 text-sm font-semibold text-amber-700 transition-colors hover:bg-amber-100"
				>
					Edit
				</button>
				<button
					onclick={() => ondelete(user.id)}
					class="rounded-lg bg-red-50 px-3.5 py-2 text-sm font-semibold text-red-700 transition-colors hover:bg-red-100"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>
