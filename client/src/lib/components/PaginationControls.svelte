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

	let {
		currentPage,
		totalPages,
		totalCount,
		itemsPerPage,
		hasNext,
		hasPrevious,
		onPageChange,
		onNext,
		onPrevious
	}: PaginationControlsProps = $props();

	const visiblePages = $derived.by(() => {
		const maxVisiblePages = 5;
		const startPage = Math.max(1, currentPage - 2);
		return Array.from(
			{ length: Math.min(maxVisiblePages, totalPages) },
			(_, i) => startPage + i
		).filter((page) => page <= totalPages);
	});

	const startItem = $derived((currentPage - 1) * itemsPerPage + 1);
	const endItem = $derived(Math.min(currentPage * itemsPerPage, totalCount));
</script>

{#if totalPages > 1}
	<div class="rounded-lg bg-white p-4">
		<div class="flex items-center justify-between">
			<div class="text-sm text-gray-600">
				Showing {startItem} to {endItem} of {totalCount} items
			</div>
			<div class="flex items-center space-x-2">
				<!-- Previous Button -->
				<button
					onclick={onPrevious}
					disabled={!hasPrevious}
					class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
				>
					<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M15 19l-7-7 7-7"
						/>
					</svg>
					Previous
				</button>

				<!-- Page Numbers -->
				<div class="flex items-center space-x-1">
					{#each visiblePages as page (page)}
						<button
							onclick={() => onPageChange(page)}
							class="inline-flex items-center rounded-md px-3 py-2 text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
							class:bg-blue-600={page === currentPage}
							class:text-white={page === currentPage}
							class:bg-white={page !== currentPage}
							class:text-gray-700={page !== currentPage}
							class:border={page !== currentPage}
							class:border-gray-300={page !== currentPage}
							class:hover:bg-gray-50={page !== currentPage}
						>
							{page}
						</button>
					{/each}
				</div>

				<!-- Next Button -->
				<button
					onclick={onNext}
					disabled={!hasNext}
					class="inline-flex items-center rounded-md border border-gray-300 bg-white px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
				>
					Next
					<svg class="ml-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M9 5l7 7-7 7"
						/>
					</svg>
				</button>
			</div>
		</div>
	</div>
{/if}
