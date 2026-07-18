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
let studentDesignator = $state("UTSG");

const handleCreateUser = async () => {
	if (!initialName.trim()) {
		return;
	}
	creatingUser = true;

	try {
		const response = await createUser(initialName, studentDesignator);
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
			<div class="space-y-4">
				<div>
					<label for="user-name" class="block text-sm font-medium text-gray-700">Person Name</label>
					<input
						type="text"
						id="user-name"
						bind:value={initialName}
						placeholder="Enter user name"
						class="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 text-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
					/>
				</div>
				<div>
					<label for="student-status" class="block text-sm font-medium text-gray-700"> Designation </label>
					<select
						id="student-status"
						bind:value={studentDesignator}
						class="mt-1 w-full rounded-md border border-gray-300 bg-white px-3 py-2 text-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
					>
						<option value="UTSG">UTSG</option>
						<option value="UTM">UTM</option>
						<option value="UTSC">UTSC</option>
						<option value="Non-UofT">Non-UofT</option>
					</select>
				</div>
			</div>

			<div class="mt-6 flex justify-end space-x-2">
				<button onclick={onClose} class="rounded-md bg-gray-200 px-4 py-2 text-sm">Cancel</button>
				<button
					onclick={handleCreateUser}
					disabled={creatingUser || !initialName.trim()}
					class="rounded-md bg-green-600 px-4 py-2 text-sm text-white disabled:bg-gray-400"
				>
					{creatingUser ? "Creating..." : "Create User"}
				</button>
			</div>
		</div>
	</div>
{/if}
