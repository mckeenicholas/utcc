<script lang="ts">
interface Props {
	message: string;
	inline?: boolean;
	minHeight?: string;
}

const { message, inline = false, minHeight = '20rem' }: Props = $props();
</script>

{#if inline}
	<div class="flex items-center justify-center py-8" style="min-height: {minHeight};">
		<div class="space-y-4 text-center">
			<p class="text-lg font-medium text-gray-700">{message}</p>
			<div class="flex justify-center">
				<div
					class="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"
				></div>
			</div>
		</div>
	</div>
{:else}
	<div class="flex min-h-screen items-center justify-center">
		<div class="w-full max-w-md space-y-4 rounded-lg bg-gray-100 p-6 text-center shadow-md">
			<p class="text-lg font-medium">{message}</p>
			<div class="flex justify-center">
				<div
					class="h-6 w-6 animate-spin rounded-full border-2 border-gray-300 border-t-gray-600"
				></div>
			</div>
		</div>
	</div>
{/if}
