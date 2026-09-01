<script lang="ts">
interface Props {
	message: string;
	inline?: boolean;
	minHeight?: string;
}

const { message, inline = false, minHeight = "16rem" }: Props = $props();
</script>

{#if inline}
	<div class="flex items-center justify-center py-8" style="min-height: {minHeight};">
		<div class="flex flex-col items-center justify-center gap-3 text-center">
			<div class="h-6 w-6 animate-spin rounded-full border-2 border-gray-200 border-t-uoft-blue"></div>
			<p class="text-xs font-medium text-gray-700">{message}</p>
		</div>
	</div>
{:else}
	<div class="flex min-h-screen items-center justify-center px-4">
		<div class="w-full max-w-sm border border-gray-200 bg-white p-8 text-center">
			<div class="flex flex-col items-center justify-center gap-3">
				<div class="h-6 w-6 animate-spin rounded-full border-2 border-gray-200 border-t-uoft-blue"></div>
				<p class="text-sm font-semibold text-gray-900">{message}</p>
			</div>
		</div>
	</div>
{/if}
