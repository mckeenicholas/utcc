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

<div class="border border-border bg-surface p-4 transition-colors hover:border-brand">
	<div class="flex items-center justify-between gap-4">
		<div class="min-w-0 flex-1">
			<div class="flex items-center gap-3">
				<div
					class="flex h-8 w-8 shrink-0 items-center justify-center rounded-sm bg-surface-muted text-xs font-bold text-brand"
				>
					{user.name.charAt(0).toUpperCase()}
				</div>
				<div class="min-w-0 flex-1">
					{#if isEditing}
						<div class="flex flex-col gap-2 sm:flex-row sm:items-center">
							<input
								bind:value={editUserName}
								onkeydown={(e) => e.key === "Enter" && handleSave()}
								class="h-9 rounded-sm border border-border-strong bg-surface px-3 py-1.5 text-xs font-medium text-main focus:border-brand focus:ring-1 focus:ring-brand focus:outline-none"
							/>
							<div class="w-32">
								<SelectMenu bind:value={editUserStudentStatus} options={studentDesignatorOptions} />
							</div>
						</div>
					{:else}
						<p class="truncate text-sm font-medium text-main">
							{user.name}
							<span class="ml-1.5 rounded-sm bg-surface-muted px-1.5 py-0.5 text-[10px] font-medium text-secondary">
								{user.student_designator}
							</span>
						</p>
					{/if}
					<p class="mt-0.5 text-[11px] font-medium text-secondary">ID: {user.id}</p>
				</div>
			</div>
		</div>
		<div class="flex shrink-0 items-center gap-1.5">
			{#if isEditing}
				<button
					type="button"
					onclick={handleSave}
					disabled={!editUserName.trim()}
					class="rounded-sm bg-uoft-blue px-2.5 py-1 text-xs font-medium text-white hover:bg-uoft-blue-80 disabled:opacity-50 dark:border dark:border-blue-500/30 dark:hover:bg-blue-900"
				>
					Save
				</button>
				<button
					type="button"
					onclick={cancelEdit}
					class="rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary hover:bg-surface-muted"
				>
					Cancel
				</button>
			{:else}
				<button
					type="button"
					onclick={startEdit}
					class="rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary hover:bg-surface-muted"
				>
					Edit
				</button>
				<button
					type="button"
					onclick={() => ondelete(user.id)}
					class="rounded-sm border border-red-200 bg-surface px-2.5 py-1 text-xs font-medium text-uoft-warm-red hover:bg-red-50 dark:border-red-900/50 dark:bg-transparent dark:text-red-400 dark:hover:bg-red-950/40"
				>
					Delete
				</button>
			{/if}
		</div>
	</div>
</div>
