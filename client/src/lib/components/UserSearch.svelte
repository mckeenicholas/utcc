<script lang="ts">
import type { User } from "$lib/types";
import { searchUsersByName } from "$lib/userService";

interface Props {
	value: string;
	onSelect: (user: User) => void;
	onClear: () => void;
	onAddUser: () => void;
	isEditMode: boolean;
	userSelected: boolean;
	searchTerm?: string;
}

let {
	value = $bindable(""),
	onSelect,
	onClear,
	onAddUser,
	isEditMode,
	userSelected,
	searchTerm = $bindable(""),
}: Props = $props();

let searchResults: User[] = $state([]);
let loading = $state(false);
let selectedIndex = $state(-1);
let showDropdown = $state(false);
let timeout: number | null = null;
let inputRef: HTMLInputElement | null = $state(null);

$effect(() => {
	if (!userSelected && inputRef) {
		inputRef.focus();
	}
});

const searchUsers = async (query: string) => {
	if (!query.trim()) {
		searchResults = [];
		return;
	}

	try {
		searchResults = await searchUsersByName(query);
	} catch (error) {
		console.error("User search failed:", error);
		searchResults = [];
	}

	loading = false;
};

const debouncedSearch = (query: string) => {
	if (timeout) {
		clearTimeout(timeout);
	}
	timeout = setTimeout(() => searchUsers(query), 300);
};

$effect(() => {
	loading = true;
	debouncedSearch(searchTerm);
});

const handleKeyDown = (event: KeyboardEvent) => {
	const totalItems = searchResults.length + (searchTerm.trim() ? 1 : 0);
	if (event.key === "ArrowDown") {
		event.preventDefault();
		selectedIndex = (selectedIndex + 1) % totalItems;
	} else if (event.key === "ArrowUp") {
		event.preventDefault();
		selectedIndex = (selectedIndex - 1 + totalItems) % totalItems;
	} else if (event.key === "Enter") {
		event.preventDefault();
		if (selectedIndex >= 0 && selectedIndex < searchResults.length) {
			onSelect(searchResults[selectedIndex]);
			showDropdown = false;
		} else if (selectedIndex === searchResults.length) {
			onAddUser();
			showDropdown = false;
		}
	} else if (event.key === "Escape") {
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
	{#if !userSelected}
		<input
			bind:this={inputRef}
			type="text"
			placeholder="Type to search users..."
			bind:value={searchTerm}
			onfocus={handleFocus}
			onblur={handleBlur}
			onkeydown={handleKeyDown}
			class="w-full rounded-sm border border-gray-300 px-3 py-1.5 text-xs text-gray-900 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
			autocomplete="off"
		/>
	{/if}

	{#if showDropdown && searchTerm.trim()}
		<div class="absolute z-10 mt-1 max-h-60 w-full overflow-y-auto rounded-sm border border-gray-200 bg-white py-1">
			{#if loading}
				<div class="px-3 py-2 text-sm text-gray-700">Searching...</div>
			{:else if searchResults.length > 0}
				{#each searchResults as user, index (user.id)}
					<button
						type="button"
						onclick={() => {
							onSelect(user);
							showDropdown = false;
						}}
						class="w-full px-3 py-2 text-left hover:bg-gray-100 {selectedIndex === index
							? 'bg-secondary-cyan-25 font-medium text-uoft-blue'
							: ''}"
					>
						{user.name}
					</button>
				{/each}
			{:else if searchTerm.trim()}
				<div class="px-3 py-2 text-sm text-gray-700">No users found</div>
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
		<div
			class="mt-2 flex items-center justify-between rounded-sm border px-3 py-1.5 text-xs {isEditMode
				? 'border-blue-200 bg-blue-50 text-uoft-blue'
				: 'border-gray-200 bg-gray-50 text-gray-900'}"
		>
			<span class="truncate">
				<span class="text-gray-700">{isEditMode ? "Editing: " : "Selected: "}</span>
				<span class="font-semibold {isEditMode ? 'text-uoft-blue' : 'text-gray-900'}">{value}</span>
			</span>
			<button
				type="button"
				onclick={() => {
					searchTerm = "";
					onClear();
				}}
				class="ml-2 inline-flex h-4 w-4 shrink-0 items-center justify-center text-sm font-bold text-gray-400 transition-colors hover:text-gray-700"
				aria-label="Clear selected competitor"
			>
				&times;
			</button>
		</div>
	{/if}
</div>
