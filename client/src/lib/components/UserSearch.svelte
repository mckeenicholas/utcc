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
			class="w-full rounded-sm border border-border-strong bg-surface px-3 py-1.5 text-xs text-main placeholder:text-muted focus:border-brand focus:ring-1 focus:ring-brand focus:outline-none"
			autocomplete="off"
		/>
	{/if}

	{#if showDropdown && searchTerm.trim()}
		<div class="absolute z-10 mt-1 max-h-60 w-full overflow-y-auto rounded-sm border border-border bg-surface py-1">
			{#if loading}
				<div class="px-3 py-2 text-sm text-secondary">Searching...</div>
			{:else if searchResults.length > 0}
				{#each searchResults as user, index (user.id)}
					<button
						type="button"
						onclick={() => {
							onSelect(user);
							showDropdown = false;
						}}
						class="w-full px-3 py-2 text-left text-main hover:bg-surface-muted {selectedIndex === index
							? 'bg-surface-muted font-medium text-brand'
							: ''}"
					>
						{user.name}
					</button>
				{/each}
			{:else if searchTerm.trim()}
				<div class="px-3 py-2 text-sm text-secondary">No users found</div>
			{/if}

			{#if searchTerm.trim()}
				<button
					type="button"
					onclick={() => {
						onAddUser();
						showDropdown = false;
					}}
					class="w-full border-t border-border px-3 py-2 text-left text-green-700 hover:bg-green-50 dark:text-green-400 dark:hover:bg-green-950/30 {selectedIndex ===
					searchResults.length
						? 'bg-green-100 dark:bg-green-950/50'
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
				? 'border-blue-200 bg-blue-50 text-uoft-blue dark:border-blue-900/60 dark:bg-blue-950/40 dark:text-blue-300'
				: 'border-border bg-surface-subtle text-main'}"
		>
			<span class="truncate">
				<span class="text-secondary">{isEditMode ? "Editing: " : "Selected: "}</span>
				<span class="font-semibold {isEditMode ? 'text-uoft-blue dark:text-blue-300' : 'text-main'}">{value}</span>
			</span>
			<button
				type="button"
				onclick={() => {
					searchTerm = "";
					onClear();
				}}
				class="ml-2 inline-flex h-4 w-4 shrink-0 items-center justify-center text-sm font-bold text-muted transition-colors hover:text-secondary"
				aria-label="Clear selected competitor"
			>
				&times;
			</button>
		</div>
	{/if}
</div>
