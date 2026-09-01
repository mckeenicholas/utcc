<script lang="ts">
import { onMount } from "svelte";
import { page } from "$app/state";
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

const loadUsers = async (pageNumber = 1) => {
	loading = true;
	try {
		const data = await fetchUsers(pageNumber);
		users = data.results;
		currentPage = pageNumber;
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
	const initialQ = page.url.searchParams.get("q");
	if (initialQ) {
		searchTerm = initialQ;
		performSearch(initialQ);
	} else {
		loadUsers(1);
	}
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
	<title>Competitors | University of Toronto Cube Club</title>
	<meta name="description" content="University of Toronto Rubik's Cube Club member search." />
</svelte:head>

<div class="py-8 pb-16">
	<div class="mx-auto max-w-6xl px-4 sm:px-6">
		<!-- Header -->
		<div class="mb-6">
			<h1 class="text-2xl font-bold tracking-tight text-gray-900 sm:text-3xl">Competitors</h1>
			<p class="mt-1 text-sm text-gray-700">Directory of club members and individual competitor records.</p>
		</div>

		<!-- Search Bar Toolbar -->
		<div class="mb-6 border border-gray-200 bg-white p-4 sm:p-5">
			<label for="search-users" class="block text-xs font-semibold tracking-wider text-gray-700 uppercase">
				Search by Name
			</label>
			<div class="mt-2">
				<input
					id="search-users"
					type="search"
					placeholder="Type competitor name..."
					bind:value={searchTerm}
					class="block w-full max-w-md rounded-sm border border-gray-200 bg-white px-3 py-2 text-sm text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
				/>
			</div>
		</div>

		<!-- Competitors Grid & Results -->
		{#if loading}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<LoadingScreen
					message={isSearching ? "Searching competitors..." : "Loading competitors..."}
					inline={true}
					minHeight="10rem"
				/>
			</div>
		{:else if users.length > 0}
			<div>
				<div class="mb-3 flex items-center justify-between border-b border-gray-200 pb-2">
					<span class="text-xs font-semibold tracking-wider text-gray-700 uppercase">
						{isSearching ? `Search Results (${totalCount})` : `All Competitors (${totalCount})`}
					</span>
				</div>

				<div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
					{#each users as user (user.id)}
						<PublicUserCard {user} />
					{/each}
				</div>

				{#if !isSearching && totalPages > 1}
					<div class="mt-6 border border-gray-200 bg-white p-4">
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
			</div>
		{:else if searchTerm.trim()}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<p class="text-base font-semibold text-gray-900">No competitors found matching "{searchTerm}"</p>
				<p class="mt-1 text-xs text-gray-700">Try searching with a different spelling or name.</p>
			</div>
		{:else}
			<div class="border border-gray-200 bg-white p-12 text-center">
				<p class="text-base font-semibold text-gray-900">No competitors found</p>
			</div>
		{/if}
	</div>
</div>
