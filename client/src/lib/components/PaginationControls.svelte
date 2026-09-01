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
	<div class="text-xs text-gray-700">
		Showing <span class="font-medium text-gray-900">{startItem}</span> to{" "}
		<span class="font-medium text-gray-900">{endItem}</span> of{" "}
		<span class="font-medium text-gray-900">{totalCount}</span>
	</div>
	<div class="flex items-center space-x-1.5">
		<!-- Previous Button -->
		<button
			type="button"
			onclick={onPrevious}
			disabled={!hasPrevious}
			class="inline-flex cursor-pointer items-center rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none disabled:cursor-not-allowed disabled:opacity-40"
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
					class="inline-flex cursor-pointer items-center rounded-sm px-2.5 py-1 text-xs font-medium transition-colors focus:outline-none"
					class:bg-uoft-blue={page === currentPage}
					class:text-white={page === currentPage}
					class:bg-white={page !== currentPage}
					class:text-gray-700={page !== currentPage}
					class:border={page !== currentPage}
					class:border-gray-200={page !== currentPage}
					class:hover:bg-gray-50={page !== currentPage}
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
			class="inline-flex cursor-pointer items-center rounded-sm border border-gray-200 bg-white px-2.5 py-1 text-xs font-medium text-gray-700 transition-colors hover:bg-gray-50 focus:outline-none disabled:cursor-not-allowed disabled:opacity-40"
		>
			Next
			<svg class="ml-1 h-3.5 w-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
			</svg>
		</button>
	</div>
</div>
