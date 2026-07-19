<script lang="ts">
import { onMount } from "svelte";
import Backbutton from "$lib/components/Backbutton.svelte";
import LoadingScreen from "$lib/components/LoadingScreen.svelte";
import PaginationControls from "$lib/components/PaginationControls.svelte";
import PublicUserCard from "$lib/components/PublicUserCard.svelte";
import type { User } from "$lib/types";
import { fetchUsers, searchUsersByName } from "$lib/userService";
import { PAGINATION_SIZE } from "$lib/utils";

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

onMount(() => {
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
</script>

<svelte:head>
	<title>UofT Rubik's Cube Club Member Search</title>
	<meta name="description" content="University of Toronto Rubik's Cube Club member search." />
</svelte:head>

<Backbutton />
<div class="min-h-screen bg-gray-50 py-8">
	<div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
		<!-- Header -->
		<div class="mb-6">
			<h1 class="text-3xl font-extrabold tracking-tight text-gray-900">Competitors</h1>
			<p class="mt-2 text-base text-gray-600">Browse all competitors and view their profiles</p>
		</div>

		<div class="mt-6 rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
			<h2 class="mb-4 text-xl font-bold text-gray-800">Search Competitors</h2>
			<div>
				<label for="search-users" class="block text-sm font-bold text-gray-700"> Search by name </label>
				<input
					id="search-users"
					placeholder="Type to search competitors..."
					bind:value={searchTerm}
					class="mt-2 block w-full rounded-lg border border-gray-300 bg-white px-3.5 py-2.5 text-sm font-medium text-gray-900 shadow-sm focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 focus:outline-none"
				/>
			</div>

			{#if loading}
				<div class="flex items-center justify-center py-10">
					<LoadingScreen message={isSearching ? "Searching..." : "Loading competitors..."} inline={true} />
				</div>
			{:else if users.length > 0}
				<div class="mt-6 space-y-3">
					<h3 class="text-sm font-bold tracking-wider text-gray-500 uppercase">
						{isSearching ? `Search Results (${totalCount})` : `All Competitors (${totalCount} total)`}
					</h3>
					<div class="mb-4 grid gap-4 sm:grid-cols-2">
						{#each users as user (user.id)}
							<PublicUserCard {user} />
						{/each}
					</div>
				</div>

				{#if !isSearching}
					{#if totalPages > 1}
						<div class="mt-6 border-t border-gray-100 pt-4">
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
				<div class="py-12 text-center text-gray-500">
					<p class="text-lg font-bold text-gray-800">No competitors found matching "{searchTerm}"</p>
					<p class="mt-2 text-sm font-medium text-gray-400">Try searching with a different name</p>
				</div>
			{:else}
				<div class="py-12 text-center text-gray-500">
					<p class="text-lg font-bold text-gray-800">No competitors found</p>
				</div>
			{/if}
		</div>
	</div>
</div>
