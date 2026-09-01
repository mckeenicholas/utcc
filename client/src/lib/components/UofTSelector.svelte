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
	status = status.includes(value) ? status.filter((v) => v !== value) : [...status, value];
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

<div class="relative w-full select-none sm:w-44">
	<!-- Trigger button -->
	<button
		type="button"
		onclick={() => (isOpen = !isOpen)}
		class="flex h-[36px] w-full cursor-pointer items-center justify-between rounded-sm border border-gray-200 bg-white px-3 py-1.5 text-left text-xs font-medium text-gray-700 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none"
	>
		<span class="truncate">{selectedLabel}</span>
		<svg
			class="ml-2 h-3.5 w-3.5 shrink-0 text-gray-400 transition-transform duration-200"
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

		<div class="absolute z-50 mt-1 max-h-60 w-full overflow-auto rounded-sm border border-gray-200 bg-white py-1">
			{#each options as option}
				<button
					type="button"
					onclick={() => toggleOption(option.value)}
					class="flex w-full cursor-pointer items-center px-3 py-1.5 text-left text-xs text-gray-700 hover:bg-gray-50 focus:outline-none"
				>
					<input
						type="checkbox"
						checked={status.includes(option.value)}
						class="pointer-events-none mr-2 h-3.5 w-3.5 rounded-sm border-gray-300 text-uoft-blue focus:ring-uoft-blue"
						readonly
					/>
					<span>{option.label}</span>
				</button>
			{/each}
		</div>
	{/if}
</div>
