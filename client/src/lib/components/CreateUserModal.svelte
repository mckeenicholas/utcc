<script lang="ts">
import { type User } from "$lib/types";
import { createUser } from "$lib/userService";

let {
	show,
	initialName = $bindable(""),
	onClose,
	onUserCreated,
}: {
	show: boolean;
	initialName?: string;
	onClose: () => void;
	onUserCreated: (user: User) => void;
} = $props();

let creatingUser = $state(false);
let isUofTStudent = $state(true);

const handleCreateUser = async () => {
	if (!initialName.trim()) {
		return;
	}
	creatingUser = true;

	try {
		const response = await createUser(initialName, isUofTStudent);
		if (response.ok) {
			const newUser: User = await response.json();
			onUserCreated(newUser);
			onClose();
		}
	} catch (error) {
		console.error("Failed to create user:", error);
	} finally {
		creatingUser = false;
	}
};
</script>

{#if show}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
		<div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
			<h3 class="mb-4 text-lg font-semibold">Add New User</h3>
			<label for="user-name" class="block text-sm font-medium text-gray-700">Person Name</label>
			<input
				type="text"
				id="user-name"
				bind:value={initialName}
				placeholder="Enter user name"
				class="w-full rounded-md border border-gray-300 px-3 py-2"
			/>
			<div class="mt-2 flex flex-row items-center">
				<label for="student-status" class="text-sm font-medium text-gray-700"> Is UofT Student? </label>
				<input id="student-status" class="ms-2 h-4 w-4" type="checkbox" bind:checked={isUofTStudent} />
			</div>

			<div class="mt-4 flex justify-end space-x-2">
				<button onclick={onClose} class="rounded-md bg-gray-200 px-4 py-2">Cancel</button>
				<button
					onclick={handleCreateUser}
					disabled={creatingUser || !initialName.trim()}
					class="rounded-md bg-green-600 px-4 py-2 text-white disabled:bg-gray-400"
				>
					{creatingUser ? "Creating..." : "Create User"}
				</button>
			</div>
		</div>
	</div>
{/if}
