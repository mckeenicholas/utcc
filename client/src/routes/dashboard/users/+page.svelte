<script lang="ts">
import { onMount } from "svelte";
import { goto } from "$app/navigation";
import AddUserForm from "$lib/components/AddUserForm.svelte";
import DashboardHeader from "$lib/components/DashboardHeader.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PaginationControls from "$lib/components/PaginationControls.svelte";
import UserCard from "$lib/components/UserCard.svelte";
import type { User } from "$lib/types";
import { createUser, deleteUserById, fetchUsers, searchUsersByName, updateUser } from "$lib/userService";
import { PAGINATION_SIZE, checkLoginStatus } from "$lib/utils";

// State Management
let users: User[] = $state([]);
let searchTerm = $state("");
let loading = $state(false);
let isSearching = $state(false);
let searchTimeout: number | null = null;

// Pagination State
let currentPage = $state(1);
let totalPages = $state(1);
let hasNext = $state(false);
let hasPrevious = $state(false);
let totalCount = $state(0);

const loadUsers = async (page = 1) => {
	loading = true;
	try {
		const data = await fetchUsers(page);
		users = data.results;
		currentPage = page;
		totalCount = data.count;
		hasNext = Boolean(data.next);
		hasPrevious = Boolean(data.previous);
		totalPages = Math.ceil(totalCount / PAGINATION_SIZE);
	} catch (error) {
		console.error("Failed to load users:", error);
		users = [];
	} finally {
		loading = false;
		isSearching = false;
	}
};

const performSearch = async (query: string) => {
	isSearching = true;
	loading = true;
	try {
		users = await searchUsersByName(query);
		// Reset pagination for search results
		currentPage = 1;
		totalPages = 1;
		hasNext = false;
		hasPrevious = false;
		totalCount = users.length;
	} catch (error) {
		console.error("Search failed:", error);
		users = [];
	} finally {
		loading = false;
	}
};

onMount(async () => {
	const loggedIn = await checkLoginStatus();

	if (!loggedIn) {
		goto("/dashboard/signin");
		return;
	}

	loadUsers(1);
});

$effect(() => {
	if (searchTimeout) {
		clearTimeout(searchTimeout);
	}

	const query = searchTerm.trim();
	if (!query) {
		// If search term is cleared, fetch all users again
		if (isSearching) {
			loadUsers(1);
		}
		return;
	}

	searchTimeout = setTimeout(() => {
		performSearch(query);
	}, 300); // 300ms debounce
});

// Event Handlers
const handleAddUser = async (name: string, studentStatus: boolean) => {
	try {
		const response = await createUser(name, studentStatus);
		if (response.ok) {
			// Refresh current view
			await (searchTerm ? performSearch(searchTerm) : loadUsers(currentPage));
		}
	} catch (error) {
		console.error("Failed to create user:", error);
		alert("Failed to create user");
	}
};

const handleSaveUser = async (userId: number, name: string, studentStatus: boolean) => {
	try {
		const response = await updateUser(userId, name, studentStatus);
		if (response.ok) {
			users = users.map((u) => (u.id === userId ? { ...u, name } : u));
		} else {
			alert("Failed to update user");
		}
	} catch (error) {
		console.error("Failed to update user:", error);
		alert("Failed to update user");
	}
};

const handleDeleteUser = async (userId: number) => {
	if (confirm("Are you sure you want to delete this user?")) {
		try {
			const response = await deleteUserById(userId);
			if (response.ok) {
				// After deleting, if the page is now empty, go to the previous page
				const willBeEmpty = users.length === 1;
				if (willBeEmpty && currentPage > 1 && !isSearching) {
					loadUsers(currentPage - 1);
				} else {
					// Otherwise, just filter out the user locally for faster UI update before a full reload
					users = users.filter((u) => u.id !== userId);
					totalCount--;
				}
			} else {
				alert("Failed to delete user");
			}
		} catch (error) {
			console.error("Failed to delete user:", error);
			alert("Failed to delete user");
		}
	}
};
</script>

<div class="min-h-screen py-8">
	<div class="mx-auto max-w-4xl px-4">
		<!-- Header -->
		<DashboardHeader title="User Management" showBack />

		<AddUserForm onAddUser={handleAddUser} />

		<div class="mt-6 rounded-lg bg-white px-6 pt-6 pb-2 shadow-sm">
			<h2 class="mb-4 text-xl font-semibold text-gray-800">Users</h2>
			<div>
				<label for="search-users" class="block text-sm font-medium text-gray-700">Search by name</label>
				<input
					id="search-users"
					placeholder="Type to search users"
					bind:value={searchTerm}
					class="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:ring-1 focus:ring-gray-500 focus:outline-none"
				/>
			</div>

			{#if loading}
				<LoadingScreen message={isSearching ? "Searching..." : "Loading users..."} />
			{:else if users.length > 0}
				<div class="mt-4 space-y-2">
					<h3 class="text-sm font-medium text-gray-700">
						{isSearching ? `Search Results (${totalCount})` : `All Users (${totalCount} total)`}
					</h3>
					<div class="grid gap-4">
						{#each users as user (user.id)}
							<UserCard {user} ondelete={handleDeleteUser} onsave={handleSaveUser} />
						{/each}
					</div>
				</div>

				{#if !isSearching}
					{#if totalPages > 1}
						<div class="mt-4">
							<PaginationControls
								{currentPage}
								{totalPages}
								{totalCount}
								itemsPerPage={PAGINATION_SIZE}
								{hasNext}
								{hasPrevious}
								onPageChange={loadUsers}
								onNext={() => loadUsers(currentPage + 1)}
								onPrevious={() => loadUsers(currentPage - 1)}
							/>
						</div>
					{/if}
				{/if}
			{:else if searchTerm.trim()}
				<div class="py-4 text-center text-gray-500">
					No users found matching "{searchTerm}"
				</div>
			{:else}
				<div class="py-4 text-center text-gray-500">No users found</div>
			{/if}
		</div>
	</div>
</div>
