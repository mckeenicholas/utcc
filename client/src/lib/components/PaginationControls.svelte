<script lang="ts">
interface PaginationControlsProps {
	currentPage: number;
	totalPages: number;
	totalCount: number;
	itemsPerPage: number;
	hasNext: boolean;
	hasPrevious: boolean;
	onPageChange: (page: number) => void;
	onNext: () => void;
	onPrevious: () => void;
}

const {
	currentPage,
	totalPages,
	totalCount,
	itemsPerPage,
	hasNext,
	hasPrevious,
	onPageChange,
	onNext,
	onPrevious,
}: PaginationControlsProps = $props();

const visiblePages = $derived.by(() => {
	const maxVisiblePages = 5;
	const startPage = Math.max(1, currentPage - 2);
	return Array.from({ length: Math.min(maxVisiblePages, totalPages) }, (_, i) => startPage + i).filter(
		(page) => page <= totalPages,
	);
});

const startItem = $derived((currentPage - 1) * itemsPerPage + 1);
const endItem = $derived(Math.min(currentPage * itemsPerPage, totalCount));
</script>

<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
	<div class="text-xs text-secondary">
		Showing <span class="font-medium text-main">{startItem}</span> to{" "}
		<span class="font-medium text-main">{endItem}</span> of{" "}
		<span class="font-medium text-main">{totalCount}</span>
	</div>
	<div class="flex items-center space-x-1.5">
		<!-- Previous Button -->
		<button
			type="button"
			onclick={onPrevious}
			disabled={!hasPrevious}
			class="inline-flex cursor-pointer items-center rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary transition-colors hover:bg-surface-muted focus:outline-none disabled:cursor-not-allowed disabled:opacity-40 dark:disabled:opacity-30"
		>
			<svg class="mr-1 h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			Prev
		</button>

		<!-- Page Numbers -->
		<div class="flex items-center space-x-1">
			{#each visiblePages as page (page)}
				<button
					type="button"
					onclick={() => onPageChange(page)}
					class="inline-flex cursor-pointer items-center rounded-sm border px-2.5 py-1 text-xs font-medium transition-colors focus:outline-none {page ===
					currentPage
						? 'border-transparent bg-uoft-blue text-white dark:border-blue-500/30'
						: 'border-border bg-surface text-secondary hover:bg-surface-muted'}"
				>
					{page}
				</button>
			{/each}
		</div>

		<!-- Next Button -->
		<button
			type="button"
			onclick={onNext}
			disabled={!hasNext}
			class="inline-flex cursor-pointer items-center rounded-sm border border-border bg-surface px-2.5 py-1 text-xs font-medium text-secondary transition-colors hover:bg-surface-muted focus:outline-none disabled:cursor-not-allowed disabled:opacity-40 dark:disabled:opacity-30"
		>
			Next
			<svg class="ml-1 h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
			</svg>
		</button>
	</div>
</div>
