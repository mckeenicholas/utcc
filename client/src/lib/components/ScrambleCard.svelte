<script lang="ts">
interface Props {
	compId: string;
	scrambleSetId: number;
	setNum: number;
	visibility: boolean;
	onSetVisibility: (vis: boolean) => void;
	onDelete: () => void;
}

const { compId, scrambleSetId, setNum, visibility, onSetVisibility, onDelete }: Props = $props();

let editing = $state(false);
let isVisible = $state(false);

$effect(() => {
	isVisible = visibility;
});

const onSave = () => {
	if (visibility !== isVisible) {
		onSetVisibility(isVisible);
	}
	editing = false;
};

const onCancel = () => {
	isVisible = visibility;
	editing = false;
};

const onEdit = () => {
	editing = true;
};

const onDeleteClick = () => {
	onDelete();
};
</script>

<div class="flex w-full items-center justify-between border-b border-gray-100 py-3 last:border-0">
	<a
		href="/dashboard/competitions/{compId}/scrambles/{scrambleSetId}"
		class="text-sm font-medium text-gray-900 transition-colors hover:text-uoft-blue"
	>
		Scramble Set {setNum}
	</a>
	<div class="flex items-center gap-2">
		{#if editing}
			<label for="{scrambleSetId}-pub-vis" class="text-xs text-gray-600">Public?</label>
			<input
				id="{scrambleSetId}-pub-vis"
				type="checkbox"
				bind:checked={isVisible}
				class="h-3.5 w-3.5 rounded-sm border-gray-300 text-uoft-blue"
			/>
			<button
				type="button"
				onclick={onSave}
				class="rounded-sm bg-uoft-blue px-2.5 py-1 text-xs font-medium text-white hover:bg-uoft-blue-80"
			>
				Save
			</button>
			<button
				type="button"
				onclick={onCancel}
				class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
			>
				Cancel
			</button>
			<button
				type="button"
				onclick={onDeleteClick}
				class="rounded-sm border border-red-200 bg-white px-2.5 py-1 text-xs font-medium text-uoft-warm-red hover:bg-red-50"
			>
				Delete
			</button>
		{:else}
			<span
				class="rounded-sm px-2 py-0.5 text-xs font-medium {isVisible
					? 'bg-green-100 text-green-800'
					: 'bg-gray-50 text-gray-400'}"
			>
				{isVisible ? "Public" : "Private"}
			</span>
			<button
				type="button"
				onclick={onEdit}
				class="rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 hover:bg-gray-50"
			>
				Edit
			</button>
		{/if}
	</div>
</div>
