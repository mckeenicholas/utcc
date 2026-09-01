<script lang="ts">
import type { ClassValue } from "svelte/elements";
import { Select } from "bits-ui";

interface Option {
	label: string;
	value: string;
}

let {
	value = $bindable(),
	options,
	placeholder = "Select...",
	class: classProps = "",
	triggerClass = "",
}: {
	value: string;
	options: Option[];
	placeholder?: string;
	class?: ClassValue;
	triggerClass?: string;
} = $props();

const selectedLabel = $derived(options.find((o) => o.value === value)?.label ?? placeholder);
</script>

<div class="relative w-full {classProps}">
	<Select.Root items={options} bind:value type="single">
		<Select.Trigger
			class="flex h-[36px] w-full cursor-pointer items-center justify-between rounded-sm border border-gray-300 bg-white px-3 py-1.5 text-left text-xs font-medium text-gray-700 focus:border-uoft-blue focus:ring-1 focus:ring-uoft-blue focus:outline-none {triggerClass}"
			aria-label={placeholder}
		>
			<span class="truncate">{selectedLabel}</span>
			<svg class="ml-2 h-3.5 w-3.5 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
			</svg>
		</Select.Trigger>
		<Select.Portal>
			<Select.Content
				class="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 z-50 max-h-96 w-[var(--bits-select-anchor-width)] min-w-[var(--bits-select-anchor-width)] overflow-hidden border border-gray-200 bg-white py-1"
				sideOffset={4}
			>
				<Select.Viewport class="p-1">
					{#each options as option (option.value)}
						<Select.Item
							class="relative flex w-full cursor-default items-center rounded-sm py-1.5 pr-2 pl-8 text-xs outline-none select-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:pointer-events-none data-[disabled]:opacity-50 data-[highlighted]:bg-gray-100"
							value={option.value}
							label={option.label}
						>
							{#snippet children({ selected })}
								{#if selected}
									<span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center text-uoft-blue">
										<svg class="h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
										</svg>
									</span>
								{/if}
								{option.label}
							{/snippet}
						</Select.Item>
					{/each}
				</Select.Viewport>
			</Select.Content>
		</Select.Portal>
	</Select.Root>
</div>
