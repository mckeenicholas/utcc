<script lang="ts">
	import authFetch from '$lib/authFetch';
	import { type User } from '$lib/types';
	import { BASE_URL } from '$lib/utils';

	let {
		show,
		initialName = '',
		onClose,
		onUserCreated
	}: {
		show: boolean;
		initialName?: string;
		onClose: () => void;
		onUserCreated: (user: User) => void;
	} = $props();

	let newUserName = $state(initialName);
	let creatingUser = $state(false);

	const createUser = async () => {
		if (!newUserName.trim()) return;
		creatingUser = true;
		try {
			const response = await authFetch(`${BASE_URL}/api/users/persons/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ name: newUserName })
			});
			if (response.ok) {
				const newUser: User = await response.json();
				onUserCreated(newUser);
				onClose();
			}
		} catch (error) {
			console.error('Failed to create user:', error);
		} finally {
			creatingUser = false;
		}
	};
</script>

{#if show}
	<div class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
		<div class="w-full max-w-md rounded-lg bg-white p-6 shadow-xl">
			<h3 class="mb-4 text-lg font-semibold">Add New User</h3>
			<input
				type="text"
				bind:value={newUserName}
				placeholder="Enter user name"
				class="w-full rounded-md border border-gray-300 px-3 py-2"
			/>
			<div class="mt-4 flex justify-end space-x-2">
				<button onclick={onClose} class="rounded-md bg-gray-200 px-4 py-2">Cancel</button>
				<button
					onclick={createUser}
					disabled={creatingUser || !newUserName.trim()}
					class="rounded-md bg-green-600 px-4 py-2 text-white disabled:bg-gray-400"
				>
					{creatingUser ? 'Creating...' : 'Create User'}
				</button>
			</div>
		</div>
	</div>
{/if}
