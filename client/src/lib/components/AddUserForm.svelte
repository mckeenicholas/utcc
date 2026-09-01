<script lang="ts">
import { studentDesignatorOptions } from "$lib/types";
import SelectMenu from "./SelectMenu.svelte";

const { onAddUser }: { onAddUser: (name: string, studentStatus: string) => Promise<void> } = $props();

let newUserName = $state("");
let newUserStudentStatus = $state("UTSG");
let isSubmitting = $state(false);

const handleSubmit = async () => {
	if (!newUserName.trim() || isSubmitting) {
		return;
	}

	isSubmitting = true;
	try {
		await onAddUser(newUserName, newUserStudentStatus);
		newUserName = "";
	} catch (error) {
		console.error("Failed to add user from form:", error);
	} finally {
		isSubmitting = false;
	}
};
</script>

<div class="border border-gray-200 bg-white p-6">
	<h2 class="mb-4 text-base font-bold text-gray-900">Add New User</h2>
	<div class="flex items-end gap-3">
		<div class="flex-1">
			<label for="new-user-name" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase"
				>Person Name</label
			>
			<input
				id="new-user-name"
				placeholder="Enter name"
				bind:value={newUserName}
				onkeydown={(e) => e.key === "Enter" && handleSubmit()}
				class="mt-1 block w-full rounded-sm border border-gray-300 px-3 py-1.5 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
			/>
		</div>
		<div class="flex w-36 flex-col">
			<label for="is-student" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase"
				>Designation</label
			>
			<div class="mt-1">
				<SelectMenu bind:value={newUserStudentStatus} options={studentDesignatorOptions} />
			</div>
		</div>
		<div>
			<button
				onclick={handleSubmit}
				disabled={isSubmitting || !newUserName.trim()}
				class="h-[36px] rounded-sm bg-uoft-blue px-4 py-1.5 text-xs font-medium text-white transition-colors hover:bg-uoft-blue-80 disabled:opacity-50"
			>
				{isSubmitting ? "Adding..." : "Add User"}
			</button>
		</div>
	</div>
</div>
