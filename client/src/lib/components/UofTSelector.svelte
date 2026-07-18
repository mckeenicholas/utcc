<script lang="ts">
let { status = $bindable() }: { status: string[] } = $props();

let isOpen = $state(false);

const options = [
	{ label: "UTSG", value: "UTSG" },
	{ label: "UTM", value: "UTM" },
	{ label: "UTSC", value: "UTSC" },
	{ label: "Non-UofT", value: "Non-UofT" },
];

const toggleOption = (value: string) => {
	if (status.includes(value)) {
		status = status.filter((v) => v !== value);
	} else {
		status = [...status, value];
	}
};

const selectedLabel = $derived.by(() => {
	if (status.length === 0 || status.length === options.length) {
		return "All Students";
	}
	return options
		.filter((o) => status.includes(o.value))
		.map((o) => o.label)
		.join(", ");
});
</script>

<div class="relative w-full select-none sm:w-48">
	<!-- Trigger button -->
	<button
		type="button"
		onclick={() => (isOpen = !isOpen)}
		class="flex h-[38px] w-full cursor-pointer items-center justify-between rounded-md border border-gray-200 bg-white px-3 py-2 text-left text-sm text-gray-700 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
	>
		<span class="truncate">{selectedLabel}</span>
		<svg
			class="ml-2 h-4 w-4 shrink-0 text-gray-400 transition-transform duration-200"
			class:rotate-180={isOpen}
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
		>
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
		</svg>
	</button>

	<!-- Dropdown Content -->
	{#if isOpen}
		<!-- Overlay to handle click outside -->
		<button
			type="button"
			class="fixed inset-0 z-40 cursor-default"
			aria-label="Close dropdown"
			tabindex="-1"
			onclick={() => (isOpen = false)}
		></button>

		<div
			class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-md border border-gray-200 bg-white py-1 shadow-lg"
		>
			{#each options as option}
				<button
					type="button"
					onclick={() => toggleOption(option.value)}
					class="flex w-full cursor-pointer items-center px-3 py-2 text-left text-sm text-gray-700 hover:bg-gray-100 focus:outline-none"
				>
					<input
						type="checkbox"
						checked={status.includes(option.value)}
						class="pointer-events-none mr-2.5 h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
						readonly
					/>
					<span>{option.label}</span>
				</button>
			{/each}
		</div>
	{/if}
</div>
