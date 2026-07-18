<script lang="ts">
import type { Session } from "$lib/types";
import type { ClassValue } from "svelte/elements";
import { Select } from "bits-ui";

const {
	value = $bindable(),
	defaultMessage = "All sessions",
	class: classProps,
	sessionData,
}: {
	value: string;
	defaultMessage?: string;
	class?: ClassValue;
	sessionData: Session[];
} = $props();

const sessions = $derived([
	{ label: defaultMessage, value: "-1" },
	...(sessionData?.map((s) => ({ label: s.name, value: s.id.toString() })) ?? []),
]);

const selectedLabel = $derived(value ? sessions.find((s) => s.value === value)?.label : defaultMessage);
</script>

<div class="w-full sm:w-48">
	<Select.Root items={sessions} bind:value type="single">
		<Select.Trigger
			class="flex w-full items-center justify-between rounded-md border border-gray-200 bg-white px-3 py-2 text-left focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none {classProps}"
			aria-label="Select an event"
		>
			<span>{selectedLabel}</span>
			<svg class="ml-2 h-4 w-4 shrink-0 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
			</svg>
		</Select.Trigger>
		<Select.Portal>
			<Select.Content
				class="data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 z-50 max-h-96 w-[var(--bits-select-anchor-width)] min-w-[var(--bits-select-anchor-width)] overflow-hidden rounded-md border border-gray-200 bg-white py-1 shadow-lg"
				sideOffset={4}
			>
				<Select.Viewport class="p-1">
					{#each sessions as option (option.value)}
						<Select.Item
							class="relative flex w-full cursor-default items-center rounded-sm py-1.5 pr-2 pl-8 text-sm outline-none select-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:pointer-events-none data-[disabled]:opacity-50 data-[highlighted]:bg-gray-100"
							value={option.value}
							label={option.label}
						>
							{#snippet children({ selected })}
								{#if selected}
									<span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
										<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
