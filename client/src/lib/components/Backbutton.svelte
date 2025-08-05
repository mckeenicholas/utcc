<script lang="ts">
	let { to }: { to: string } = $props();
</script>

<div class="ms-2 mt-2">
	<a
		href={to}
		class="inline-flex items-center rounded-md bg-gray-600 py-2 pe-4 ps-3 text-sm font-medium text-white transition-colors duration-150 hover:bg-gray-700"
	>
		<svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
		</svg>
		Back
	</a>
</div>
