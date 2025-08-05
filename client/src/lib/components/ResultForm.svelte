<script lang="ts">
	import type { WCAEvent, Result } from '$lib/types';
	import { eventNames, eventSolves } from '$lib/types';
	import { Select } from 'bits-ui';
	import ResultEntryField from './ResultEntryField.svelte';

	interface Props {
		formData: {
			name: string;
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
		onFormDataChange: (key: string, value: unknown) => void;
	}

	let { formData, editingResult, submitting, onSubmit, onCancel, onFormDataChange }: Props =
		$props();

	// Computed property for number of attempts
	const getAttemptCount = (event: WCAEvent): number => {
		return eventSolves[event] || 5;
	};

	// Prepare event options for Select component
	const eventOptions = Object.entries(eventNames).map(([key, name]) => ({
		value: key,
		label: name
	}));

	const selectedEventLabel = $derived.by(() => {
		const selected = eventOptions.find((option) => option.value === formData.event);
		return selected ? selected.label : 'Select an event';
	});

	// Computed property to check if required fields are filled
	const areRequiredFieldsFilled = $derived(
		formData.name.trim() !== '' && formData.event && formData.round > 0
	);
</script>

<div class="submit-form rounded-lg bg-white p-6 shadow-sm">
	<div class="mb-6 flex items-center justify-between">
		<h2 class="text-xl font-semibold text-gray-800">
			{editingResult ? 'Edit Result' : 'Submit Result'}
		</h2>
		{#if editingResult}
			<button onclick={onCancel} class="text-sm text-gray-500 hover:text-gray-700">
				Cancel Edit
			</button>
		{/if}
	</div>

	{#if editingResult}
		<div class="mb-4 rounded-md border border-blue-200 bg-blue-50 p-3">
			<p class="text-sm text-blue-800">
				Editing: <span class="font-medium">{editingResult.name}</span> -
				{eventNames[editingResult.event as WCAEvent]} Round {editingResult.round}
			</p>
		</div>
	{/if}
	<div class="space-y-4">
		<div>
			<label for="name" class="mb-2 block text-sm font-medium text-gray-700">Name</label>
			<input
				id="name"
				type="text"
				value={formData.name}
				oninput={(e) => onFormDataChange('name', (e.target as HTMLInputElement).value)}
				placeholder="Enter competitor name"
				class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
			/>
		</div>

		<div>
			<label for="event" class="mb-2 block text-sm font-medium text-gray-700">Event</label>
			<Select.Root
				type="single"
				onValueChange={(v) => onFormDataChange('event', v)}
				items={eventOptions}
			>
				<Select.Trigger
					class="flex w-full items-center justify-between rounded-md border border-gray-300 bg-white px-3 py-2 text-left shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
					aria-label="Select an event"
				>
					<span>{selectedEventLabel}</span>
					<svg
						class="ml-2 h-4 w-4 flex-shrink-0 text-gray-400"
						fill="none"
						stroke="currentColor"
						viewBox="0 0 24 24"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M19 9l-7 7-7-7"
						/>
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
									class="relative flex w-full cursor-default select-none items-center rounded-sm py-1.5 pl-8 pr-2 text-sm outline-none hover:bg-gray-100 focus:bg-gray-100 data-[disabled]:pointer-events-none data-[highlighted]:bg-gray-100 data-[disabled]:opacity-50"
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
				value={formData.round}
				oninput={(e) => onFormDataChange('round', (e.target as HTMLInputElement).value)}
				class="block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
			/>
		</div>
	</div>

	<!-- Time Inputs -->
	<div class="mt-6">
		<h3 class="mb-4 text-lg font-medium text-gray-800">Times</h3>
		<div class="space-y-3">
			<div>
				<label for="time1" class="mb-2 block text-sm font-medium text-gray-700">Time 1</label>
				<ResultEntryField
					id="time1"
					bind:value={() => formData.time1, (v) => onFormDataChange('time1', v)}
					placeholder="Enter time 1"
					disabled={!areRequiredFieldsFilled}
				/>
			</div>
			<div>
				<label for="time2" class="mb-2 block text-sm font-medium text-gray-700">Time 2</label>
				<ResultEntryField
					id="time2"
					bind:value={() => formData.time2, (v) => onFormDataChange('time2', v)}
					placeholder="Enter time 2"
					disabled={!areRequiredFieldsFilled}
				/>
			</div>
			<div>
				<label for="time3" class="mb-2 block text-sm font-medium text-gray-700">Time 3</label>
				<ResultEntryField
					id="time3"
					bind:value={() => formData.time3, (v) => onFormDataChange('time3', v)}
					placeholder="Enter time 3"
					disabled={!areRequiredFieldsFilled}
				/>
			</div>
			{#if getAttemptCount(formData.event) === 5}
				<div>
					<label for="time4" class="mb-2 block text-sm font-medium text-gray-700">Time 4</label>
					<ResultEntryField
						id="time4"
						bind:value={() => formData.time4, (v) => onFormDataChange('time4', v)}
						placeholder="Enter time 4"
						disabled={!areRequiredFieldsFilled}
					/>
				</div>
				<div>
					<label for="time5" class="mb-2 block text-sm font-medium text-gray-700">Time 5</label>
					<ResultEntryField
						id="time5"
						bind:value={() => formData.time5, (v) => onFormDataChange('time5', v)}
						placeholder="Enter time 5"
						disabled={!areRequiredFieldsFilled}
					/>
				</div>
			{/if}
		</div>
	</div>

	<div class="mt-6">
		<button
			onclick={onSubmit}
			disabled={submitting || !areRequiredFieldsFilled}
			class="submit-button inline-flex w-full items-center justify-center rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:bg-gray-400"
		>
			{#if submitting}
				<svg
					class="mr-2 h-4 w-4 animate-spin"
					fill="none"
					stroke="currentColor"
					viewBox="0 0 24 24"
				>
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
					/>
				</svg>
				{editingResult ? 'Updating...' : 'Submitting...'}
			{:else}
				{editingResult ? 'Update Result' : 'Submit Result'}
			{/if}
		</button>
		{#if editingResult}
			<button
				onclick={onCancel}
				disabled={submitting}
				class="mt-3 inline-flex w-full items-center justify-center rounded-md bg-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50"
			>
				Cancel
			</button>
		{/if}
	</div>
</div>
