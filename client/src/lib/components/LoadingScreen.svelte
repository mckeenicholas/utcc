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
			<div class="h-6 w-6 animate-spin rounded-full border-2 border-border border-t-brand"></div>
			<p class="text-xs font-medium text-secondary">{message}</p>
		</div>
	</div>
{:else}
	<div class="flex min-h-screen items-center justify-center px-4">
		<div class="w-full max-w-sm border border-border bg-surface p-8 text-center">
			<div class="flex flex-col items-center justify-center gap-3">
				<div class="h-6 w-6 animate-spin rounded-full border-2 border-border border-t-brand"></div>
				<p class="text-sm font-semibold text-main">{message}</p>
			</div>
		</div>
	</div>
{/if}
