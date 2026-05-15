<script lang="ts">
	import type { WCAEvent, Result } from "$lib/types";
	import { eventNames, eventSolves } from "$lib/types";
	import { Select } from "bits-ui";
	import ResultEntryField from "./ResultEntryField.svelte";

	interface Props {
		formData: {
			event: WCAEvent;
			round: number;
			time1: number;
			time2: number;
			time3: number;
			time4: number;
			time5: number;
		};
		editingResult: Result | null;
		submitting: boolean;
		onSubmit: () => void;
		onCancel: () => void;
		additionalValidation?: boolean;
	}

	let {
		formData = $bindable(),
		editingResult,
		submitting,
		onSubmit,
		onCancel,
		additionalValidation = true,
	}: Props = $props();

	const getAttemptCount = (event: WCAEvent): number => {
		return eventSolves[event] || 5;
	};

	const eventOptions = Object.entries(eventNames).map(([key, name]) => ({
		value: key,
		label: name,
	}));

	const selectedEventLabel = $derived.by(() => {
		const selected = eventOptions.find((option) => option.value === formData.event);
		return selected ? selected.label : "Select an event";
	});

	const areRequiredFieldsFilled = $derived(formData.event && formData.round > 0 && additionalValidation);

	const handleKeydown = (event: KeyboardEvent) => {
		if (event.key === "Enter") {
			onSubmit();
		} else if (event.key === "ArrowUp" || event.key === "-") {
			event.preventDefault();
			const inputs = document.querySelectorAll(".time-input");
			const currentIndex = Array.from(inputs).indexOf(event.target as HTMLInputElement);
			const prevInput = inputs[currentIndex - 1] as HTMLInputElement;
			if (prevInput) {
				prevInput.focus();
			}
		}
	};
</script>

<div class="my-4 flex items-center justify-between">
	<h2 class="text-lg font-semibold text-gray-800">
		{editingResult ? "Edit Results" : "Enter Results"}
	</h2>
</div>

<div class="space-y-4">
	<div>
		<label for="event" class="mb-2 block text-sm font-medium text-gray-700">Event</label>
		<Select.Root items={eventOptions} bind:value={formData.event} type="single">
			<Select.Trigger
				class="flex w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-left shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
				aria-label="Select an event"
			>
				<span>{selectedEventLabel}</span>
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
						{#each eventOptions as option (option.value)}
							<Select.Item
								class="relative flex w-full cursor-default items-center rounded-sm py-1.5 pr-2 pl-8 text-sm outline-none select-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:pointer-events-none data-[disabled]:opacity-50 data-[highlighted]:bg-gray-100"
								value={option.value}
								label={option.label}
							>
								{#snippet children({ selected })}
									{#if selected}
										<span class="absolute left-2 flex h-3.5 w-3.5 items-center justify-center">
											<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="2"
													d="M5 13l4 4L19 7"
												/>
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

	<div>
		<label for="round" class="mb-2 block text-sm font-medium text-gray-700">Round</label>
		<input
			id="round"
			type="number"
			min="1"
			bind:value={formData.round}
			class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
		/>
	</div>
</div>

<!-- Time Inputs -->
<div class="mt-4">
	<h3 class="mb-4 text-lg font-medium text-gray-800">Times</h3>
	<div class="space-y-3">
		<div>
			<label for="time1" class="mb-1 block text-sm font-medium text-gray-700">Time 1</label>
			<ResultEntryField
				id="time1"
				bind:value={formData.time1}
				placeholder="Enter time 1"
				disabled={!areRequiredFieldsFilled}
			/>
		</div>
		<div>
			<label for="time2" class="mb-1 block text-sm font-medium text-gray-700">Time 2</label>
			<ResultEntryField
				id="time2"
				bind:value={formData.time2}
				placeholder="Enter time 2"
				disabled={!areRequiredFieldsFilled}
			/>
		</div>
		<div>
			<label for="time3" class="mb-1 block text-sm font-medium text-gray-700">Time 3</label>
			<ResultEntryField
				id="time3"
				bind:value={formData.time3}
				placeholder="Enter time 3"
				disabled={!areRequiredFieldsFilled}
			/>
		</div>
		{#if getAttemptCount(formData.event) === 5}
			<div>
				<label for="time4" class="mb-1 block text-sm font-medium text-gray-700">Time 4</label>
				<ResultEntryField
					id="time4"
					bind:value={formData.time4}
					placeholder="Enter time 4"
					disabled={!areRequiredFieldsFilled}
				/>
			</div>
			<div>
				<label for="time5" class="mb-1 block text-sm font-medium text-gray-700">Time 5</label>
				<ResultEntryField
					id="time5"
					bind:value={formData.time5}
					placeholder="Enter time 5"
					disabled={!areRequiredFieldsFilled}
				/>
			</div>
		{/if}
	</div>
</div>

<div class="mt-4">
	<button
		onclick={onSubmit}
		onkeydown={handleKeydown}
		disabled={submitting || !areRequiredFieldsFilled}
		class="time-input submit-button inline-flex w-full items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-400"
	>
		{#if submitting}
			<svg class="mr-2 h-4 w-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
				/>
			</svg>
			{editingResult ? "Updating..." : "Submitting..."}
		{:else}
			{editingResult ? "Update Result" : "Submit Result"}
		{/if}
	</button>
	{#if editingResult}
		<button
			onclick={onCancel}
			disabled={submitting}
			class="mt-3 inline-flex w-full items-center justify-center rounded-md bg-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-300 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none disabled:opacity-50"
		>
			Cancel
		</button>
	{/if}
</div>
