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

<div class="flex w-full items-center justify-between">
	<a
		href="/dashboard/competitions/{compId}/scrambles/{scrambleSetId}"
		class="me-2 grow cursor-pointer p-2 ps-6 transition-colors ease-in-out hover:bg-gray-200"
	>
		Set {setNum}
	</a>
	<div class="me-2 flex items-center gap-2">
		{#if editing}
			<label for="{scrambleSetId}-pub-vis">Is Publicly Visible?</label>
			<input id="{scrambleSetId}-pub-vis" type="checkbox" bind:checked={isVisible} class="me-2" />
			<button onclick={onSave}>
				<div class="rounded-md bg-green-100 px-3 py-1 text-sm text-green-800 hover:bg-green-200">Save</div>
			</button>
			<button onclick={onDeleteClick}>
				<div class="rounded-md bg-red-100 px-3 py-1 text-sm text-red-800 hover:bg-red-200">Delete</div>
			</button>
			<button onclick={onCancel}>
				<div class="rounded-md bg-yellow-100 px-3 py-1 text-sm text-yellow-800 hover:bg-yellow-200">Cancel</div>
			</button>
		{:else}
			<div
				class="rounded-md px-3 py-1 text-sm {isVisible ? 'bg-red-100  text-red-800' : 'bg-green-100  text-green-800'}"
			>
				{isVisible ? "Publicly Visible" : "Private"}
			</div>
			<button onclick={onEdit}>
				<div class="rounded-md bg-blue-100 px-3 py-1 text-sm text-blue-800 hover:bg-blue-200">Edit Info</div>
			</button>
		{/if}
	</div>
</div>
