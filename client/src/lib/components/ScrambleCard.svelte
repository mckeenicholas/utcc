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

<div class="flex w-full items-center justify-between border-b border-border py-3 last:border-0">
	<a
		href="/dashboard/competitions/{compId}/scrambles/{scrambleSetId}"
		class="text-sm font-medium text-main transition-colors hover:text-brand"
	>
		Scramble Set {setNum}
	</a>
	<div class="flex items-center gap-2">
		{#if editing}
			<label for="{scrambleSetId}-pub-vis" class="text-xs text-secondary">Public?</label>
			<input
				id="{scrambleSetId}-pub-vis"
				type="checkbox"
				bind:checked={isVisible}
				class="h-3.5 w-3.5 rounded-sm border-border-strong bg-surface text-uoft-blue"
			/>
			<button
				type="button"
				onclick={onSave}
				class="rounded-sm bg-uoft-blue px-2.5 py-1 text-xs font-medium text-white hover:bg-uoft-blue-80 dark:border dark:border-blue-500/30"
			>
				Save
			</button>
			<button
				type="button"
				onclick={onCancel}
				class="rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary hover:bg-surface-muted"
			>
				Cancel
			</button>
			<button
				type="button"
				onclick={onDeleteClick}
				class="rounded-sm border border-red-200 bg-surface px-2.5 py-1 text-xs font-medium text-uoft-warm-red hover:bg-red-50 dark:border-red-900/60 dark:text-red-400 dark:hover:bg-red-950/40"
			>
				Delete
			</button>
		{:else}
			<span
				class="rounded-sm px-2 py-0.5 text-xs font-medium {isVisible
					? 'bg-green-100 text-green-800 dark:bg-green-950/60 dark:text-green-300'
					: 'bg-surface-subtle text-muted'}"
			>
				{isVisible ? "Public" : "Private"}
			</span>
			<button
				type="button"
				onclick={onEdit}
				class="rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary hover:bg-surface-muted"
			>
				Edit
			</button>
		{/if}
	</div>
</div>
