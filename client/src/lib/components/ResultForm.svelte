<script lang="ts">
import { eventSolves, type Result, type WCAEvent } from "$lib/types";
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

const {
	formData = $bindable(),
	editingResult,
	submitting,
	onSubmit,
	onCancel,
	additionalValidation = true,
}: Props = $props();

const getAttemptCount = (event: WCAEvent): number => eventSolves[event] || 5;

const areRequiredFieldsFilled = $derived(formData.event && formData.round > 0 && additionalValidation);

const handleKeydown = (event: KeyboardEvent) => {
	if (event.key === "Enter") {
		onSubmit();
	} else if (event.key === "ArrowUp" || event.key === "-") {
		event.preventDefault();
		const inputs = document.querySelectorAll(".time-input");
		const currentIndex = [...inputs].indexOf(event.target as HTMLInputElement);
		const prevInput = inputs[currentIndex - 1] as HTMLInputElement;
		if (prevInput) {
			prevInput.focus();
		}
	}
};
</script>

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
