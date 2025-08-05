<script lang="ts">
	import authFetch from '$lib/authFetch';
	import type { User, Paginated } from '$lib/types';
	import { BASE_URL, PAGINATION_SIZE } from '$lib/utils';

	let searchTerm = $state('');
	let loading = $state(false);
	let newUserName = $state('');
	let users: User[] = $state([]);
	let searchTimeout: number | null = null;
	let editingUser: number | null = $state(null);
	let editUserName = $state('');

	// Pagination state
	let currentPage = $state(1);
	let totalPages = $state(1);
	let hasNext = $state(false);
	let hasPrevious = $state(false);
	let totalCount = $state(0);
	let isSearching = $state(false);

	const fetchAllUsers = async (page: number = 1) => {
		loading = true;
		try {
			const response = await fetch(`${BASE_URL}/api/users/persons/?page=${page}`);
			const data: Paginated<User> = await response.json();

			users = data.results;
			currentPage = page;
			totalCount = data.count;
			hasNext = !!data.next;
			hasPrevious = !!data.previous;
			totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
		} catch (error) {
			console.error('Failed to fetch users:', error);
			users = [];
		} finally {
			loading = false;
		}
	};

	const searchUsers = async (query: string) => {
		if (!query.trim()) {
			isSearching = false;
			fetchAllUsers(1);
			return;
		}

		isSearching = true;
		loading = true;
		try {
			const response = await fetch(
				`${BASE_URL}/api/users/persons/search/?name=${encodeURIComponent(query)}`
			);
			const data = await response.json();
			users = data.results || data || [];
			// Reset pagination for search results
			currentPage = 1;
			totalPages = 1;
			hasNext = false;
			hasPrevious = false;
			totalCount = users.length;
		} catch (error) {
			console.error('Search failed:', error);
			users = [];
		} finally {
			loading = false;
		}
	};

	const debouncedSearch = (query: string) => {
		if (searchTimeout) {
			clearTimeout(searchTimeout);
		}

		searchTimeout = setTimeout(() => {
			searchUsers(query);
		}, 300); // 300ms debounce
	};

	// Reactive effect to trigger search when searchTerm changes
	$effect(() => {
		debouncedSearch(searchTerm);
	});

	// Load initial users on mount
	$effect(() => {
		if (!searchTerm.trim()) {
			fetchAllUsers(1);
		}
	});

	const goToNextPage = () => {
		if (hasNext && !isSearching) {
			fetchAllUsers(currentPage + 1);
		}
	};

	const goToPreviousPage = () => {
		if (hasPrevious && !isSearching) {
			fetchAllUsers(currentPage - 1);
		}
	};

	const createNewUser = async () => {
		try {
			const response = await authFetch(`${BASE_URL}/api/users/persons/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: newUserName })
			});

			if (response.ok) {
				newUserName = '';
				// Refresh search results if there's a current search, otherwise refresh all users
				if (searchTerm.trim()) {
					searchUsers(searchTerm);
				} else {
					fetchAllUsers(currentPage);
				}
			}
		} catch (error) {
			console.error('Failed to create user:', error);
		}
	};

	const deleteUser = async (userId: number) => {
		if (confirm('Are you sure you want to delete this user?')) {
			try {
				const response = await authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
					method: 'DELETE',
					headers: {
						'Content-Type': 'application/json'
					}
				});

				if (response.ok) {
					users = users.filter((u) => u.id !== userId);
					// Update total count
					totalCount = Math.max(0, totalCount - 1);

					// If this was the last user on the current page and there are previous pages, go back one page
					if (users.length === 0 && currentPage > 1 && !isSearching) {
						fetchAllUsers(currentPage - 1);
					}
				} else {
					alert('Failed to delete user');
				}
			} catch (error) {
				console.error('Failed to delete user:', error);
				alert('Failed to delete user');
			}
		}
	};

	const startEditUser = (user: User) => {
		editingUser = user.id;
		editUserName = user.name;
	};

	const cancelEdit = () => {
		editingUser = null;
		editUserName = '';
	};

	const saveUser = async (userId: number) => {
		try {
			const response = await authFetch(`${BASE_URL}/api/users/persons/${userId}/`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ name: editUserName })
			});

			if (response.ok) {
				// Update the user in the array
				users = users.map((u) => (u.id === userId ? { ...u, name: editUserName } : u));
				editingUser = null;
				editUserName = '';
			} else {
				alert('Failed to update user');
			}
		} catch (error) {
			console.error('Failed to update user:', error);
			alert('Failed to update user');
		}
	};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<!-- Header -->
		<div class="mb-8 flex items-center justify-between">
			<h1 class="text-3xl font-bold text-gray-900">User Management</h1>
			<a
				href="/dashboard"
				class="rounded-md bg-gray-600 px-4 py-2 text-white hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
			>
				Back to Dashboard
			</a>
		</div>

		<!-- Add New User Section -->
		<div class="rounded-lg bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-semibold text-gray-800">Add New User</h2>
			<div class="space-y-4">
				<div class="flex gap-3">
					<div class="flex-1">
						<label for="new-user-name" class="block text-sm font-medium text-gray-700"
							>Person Name</label
						>
						<input
							id="new-user-name"
							placeholder="Enter name"
							bind:value={newUserName}
							class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
						/>
					</div>
					<div class="flex items-end">
						<button
							onclick={createNewUser}
							disabled={!newUserName}
							class="rounded-md bg-green-600 px-4 py-2 text-white hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400"
						>
							Add User
						</button>
					</div>
				</div>
			</div>
		</div>

		<!-- Search Users Section -->
		<div class="mt-6 rounded-lg bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-semibold text-gray-800">Search Users</h2>
			<div class="space-y-4">
				<div>
					<label for="search-users" class="block text-sm font-medium text-gray-700"
						>Search by name</label
					>
					<input
						id="search-users"
						placeholder="Type to search users"
						bind:value={searchTerm}
						class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
					/>
				</div>

				{#if loading}
					<div class="flex items-center justify-center py-4">
						<div
							class="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"
						></div>
						<span class="ml-2 text-gray-600"
							>{isSearching ? 'Searching...' : 'Loading users...'}</span
						>
					</div>
				{:else if isSearching && searchTerm.trim() && users.length === 0}
					<div class="py-4 text-center text-gray-500">
						No users found matching "{searchTerm}"
					</div>
				{:else if users.length > 0}
					<div class="space-y-2">
						<h3 class="text-sm font-medium text-gray-700">
							{isSearching ? `Search Results (${users.length})` : `All Users (${totalCount} total)`}
						</h3>
						<div class="grid gap-4">
							{#each users as user (user.id)}
								<div
									class="rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md"
								>
									<div class="flex items-center justify-between">
										<div class="flex items-center space-x-3">
											<div
												class="flex h-10 w-10 items-center justify-center rounded-full bg-blue-100 text-lg font-medium text-blue-600"
											>
												{user.name.charAt(0).toUpperCase()}
											</div>
											<div>
												{#if editingUser === user.id}
													<input
														bind:value={editUserName}
														class="rounded-md border border-gray-300 px-2 py-1 text-sm font-medium text-gray-900 focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
													/>
												{:else}
													<p class="text-sm font-medium text-gray-900">{user.name}</p>
												{/if}
												<p class="text-xs text-gray-500">ID: {user.id}</p>
											</div>
										</div>
										<div class="flex space-x-2">
											{#if editingUser === user.id}
												<button
													onclick={() => saveUser(user.id)}
													disabled={!editUserName.trim()}
													class="rounded-md bg-green-100 px-3 py-1 text-sm text-green-800 hover:bg-green-200 disabled:cursor-not-allowed disabled:bg-gray-200 disabled:text-gray-500"
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
													onclick={() => startEditUser(user)}
													class="rounded-md bg-yellow-100 px-3 py-1 text-sm text-yellow-800 hover:bg-yellow-200"
												>
													Edit
												</button>
												<button
													onclick={() => deleteUser(user.id)}
													class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200"
												>
													Delete
												</button>
											{/if}
										</div>
									</div>
								</div>
							{/each}
						</div>
					</div>

					<!-- Pagination Controls -->
					{#if !isSearching && totalPages > 1}
						<div
							class="mt-6 flex items-center justify-between rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
						>
							<div class="text-sm text-gray-500">
								Showing page {currentPage} of {totalPages} ({totalCount} total users)
							</div>
							<div class="flex space-x-2">
								<button
									onclick={goToPreviousPage}
									disabled={!hasPrevious}
									class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:text-gray-400"
								>
									<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M15 19l-7-7 7-7"
										/>
									</svg>
									Previous
								</button>
								<button
									onclick={goToNextPage}
									disabled={!hasNext}
									class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:text-gray-400"
								>
									Next
									<svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M9 5l7 7-7 7"
										/>
									</svg>
								</button>
							</div>
						</div>
					{/if}
				{:else if !isSearching}
					<div class="py-4 text-center text-gray-500">No users found</div>
				{/if}
			</div>
		</div>
	</div>
</div>
