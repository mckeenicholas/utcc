<script lang="ts">
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

<div class="rounded-lg bg-white p-6 shadow-sm">
	<h2 class="mb-4 text-xl font-semibold text-gray-800">Add New User</h2>
	<div class="flex items-end gap-3">
		<div class="flex-1">
			<label for="new-user-name" class="block text-sm font-medium text-gray-700">Person Name</label>
			<input
				id="new-user-name"
				placeholder="Enter name"
				bind:value={newUserName}
				onkeydown={(e) => e.key === "Enter" && handleSubmit()}
				class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
			/>
		</div>
		<div class="flex w-36 flex-col">
			<label for="is-student" class="block text-sm font-medium text-gray-700">Designation</label>
			<select
				bind:value={newUserStudentStatus}
				id="is-student"
				class="mt-1 block w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
			>
				<option value="UTSG">UTSG</option>
				<option value="UTM">UTM</option>
				<option value="UTSC">UTSC</option>
				<option value="Non-UofT">Non-UofT</option>
			</select>
		</div>
		<div>
			<button
				onclick={handleSubmit}
				disabled={!newUserName.trim() || isSubmitting}
				class="h-[38px] rounded-md bg-green-600 px-4 py-2 text-sm text-white hover:bg-green-700 focus:ring-2 focus:ring-green-500 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-400"
			>
				{isSubmitting ? "Adding..." : "Add User"}
			</button>
		</div>
	</div>
</div>
