<script lang="ts">
	import type { User } from '$lib/types';

	let {
		value = '',
		onSelect,
		onClear,
		onAddUser
	}: {
		value: string;
		onSelect: (user: User) => void;
		onClear: () => void;
		onAddUser: () => void;
	} = $props();

	let searchTerm = $state(value);
	let searchResults: User[] = $state([]);
	let loading = $state(false);
	let selectedIndex = $state(-1);
	let showDropdown = $state(false);
	let timeout: number | null = null;

	const searchUsers = async (query: string) => {
		if (!query.trim()) {
			searchResults = [];
			return;
		}
		loading = true;
		try {
			const response = await fetch(`/api/users/persons/search/?name=${encodeURIComponent(query)}`);
			const data = await response.json();
			searchResults = data.results || data || [];
		} catch (error) {
			console.error('User search failed:', error);
			searchResults = [];
		} finally {
			loading = false;
		}
	};

	const debouncedSearch = (query: string) => {
		if (timeout) clearTimeout(timeout);
		timeout = setTimeout(() => searchUsers(query), 300);
	};

	$effect(() => {
		debouncedSearch(searchTerm);
	});

	const handleKeyDown = (event: KeyboardEvent) => {
		const totalItems = searchResults.length + (searchTerm.trim() ? 1 : 0);
		if (event.key === 'ArrowDown') {
			event.preventDefault();
			selectedIndex = (selectedIndex + 1) % totalItems;
		} else if (event.key === 'ArrowUp') {
			event.preventDefault();
			selectedIndex = (selectedIndex - 1 + totalItems) % totalItems;
		} else if (event.key === 'Enter') {
			event.preventDefault();
			if (selectedIndex >= 0 && selectedIndex < searchResults.length) {
				onSelect(searchResults[selectedIndex]);
				showDropdown = false;
			} else if (selectedIndex === searchResults.length) {
				onAddUser();
				showDropdown = false;
			}
		} else if (event.key === 'Escape') {
			showDropdown = false;
		}
	};

	const handleFocus = () => {
		showDropdown = true;
	};

	const handleBlur = () => {
		setTimeout(() => (showDropdown = false), 200);
	};
</script>

<div class="relative">
	<input
		type="text"
		placeholder="Type to search users..."
		bind:value={searchTerm}
		onfocus={handleFocus}
		onblur={handleBlur}
		onkeydown={handleKeyDown}
		class="w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-gray-500 focus:outline-none focus:ring-1 focus:ring-gray-500"
		autocomplete="off"
	/>

	{#if showDropdown}
		<div
			class="absolute z-10 mt-1 max-h-60 w-full overflow-y-auto rounded-md border border-gray-300 bg-white shadow-lg"
		>
			{#if loading}
				<div class="px-3 py-2 text-sm text-gray-500">Searching...</div>
			{:else if searchResults.length > 0}
				{#each searchResults as user, index (user.id)}
					<button
						type="button"
						onclick={() => {
							onSelect(user);
							showDropdown = false;
						}}
						class="w-full px-3 py-2 text-left hover:bg-gray-100 {selectedIndex === index
							? 'bg-blue-100'
							: ''}"
					>
						{user.name}
					</button>
				{/each}
			{:else if searchTerm.trim()}
				<div class="px-3 py-2 text-sm text-gray-500">No users found</div>
			{/if}

			{#if searchTerm.trim()}
				<button
					type="button"
					onclick={() => {
						onAddUser();
						showDropdown = false;
					}}
					class="w-full border-t border-gray-200 px-3 py-2 text-left text-green-700 hover:bg-green-50 {selectedIndex ===
					searchResults.length
						? 'bg-green-100'
						: ''}"
				>
					Add new user: "{searchTerm}"
				</button>
			{/if}
		</div>
	{/if}

	{#if value}
		<div class="mt-2 flex items-center justify-between rounded-md bg-green-50 px-3 py-2">
			<span class="text-sm text-green-800">{value}</span>
			<button type="button" onclick={onClear} class="text-green-600 hover:text-green-800">
				&times;
			</button>
		</div>
	{/if}
</div>
