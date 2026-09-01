<script lang="ts">
import { type User, studentDesignatorOptions } from "$lib/types";
import SelectMenu from "./SelectMenu.svelte";

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

<div class="border border-gray-200 bg-white p-4 transition-colors hover:border-uoft-blue">
	<div class="flex items-center justify-between gap-4">
		<div class="min-w-0 flex-1">
			<div class="flex items-center gap-3">
				<div
					class="flex h-8 w-8 shrink-0 items-center justify-center rounded-sm bg-gray-100 text-xs font-bold text-uoft-blue"
				>
					{user.name.charAt(0).toUpperCase()}
				</div>
				<div class="min-w-0 flex-1">
					{#if isEditing}
						<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
							<input
								bind:value={editUserName}
								onkeydown={(e) => e.key === "Enter" && handleSave()}
								class="h-[36px] rounded-sm border border-gray-300 px-3 py-1.5 text-xs font-medium text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
							/>
							<div class="w-32">
								<SelectMenu bind:value={editUserStudentStatus} options={studentDesignatorOptions} />
							</div>
						</div>
					{:else}
						<p class="truncate text-sm font-medium text-gray-900">
							{user.name}
							<span class="ml-1.5 rounded-sm bg-gray-100 px-1.5 py-0.5 text-[10px] font-medium text-gray-600">
								{user.student_designator}
							</span>
						</p>
					{/if}
					<p class="mt-0.5 text-[11px] font-medium text-gray-700">ID: {user.id}</p>
				</div>
			</div>
		</div>
		<div class="flex shrink-0 items-center gap-1.5">
			{#if isEditing}
				<button
					type="button"
					onclick={handleSave}
					disabled={!editUserName.trim()}
					class="rounded-sm bg-uoft-blue px-2.5 py-1 text-xs font-medium text-white hover:bg-uoft-blue-80 disabled:opacity-50"
				>
					Save
				</button>
				<button
					type="button"
					onclick={cancelEdit}
					class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
				>
					Cancel
				</button>
			{:else}
				<button
					type="button"
					onclick={startEdit}
					class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
				>
					Edit
				</button>
				<button
					type="button"
					onclick={() => ondelete(user.id)}
					class="rounded-sm border border-red-200 bg-white px-2.5 py-1 text-xs font-medium text-uoft-warm-red hover:bg-red-50"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>
