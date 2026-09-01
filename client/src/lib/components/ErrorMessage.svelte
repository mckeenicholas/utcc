<script lang="ts">
interface Props {
	message: string | null;
}

const { message }: Props = $props();
</script>

{#if message}
	<div class="mb-6 rounded-sm border border-red-200 bg-red-50 p-3.5">
		<div class="flex items-center gap-3">
			<div class="shrink-0 text-uoft-warm-red">
				<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"
					/>
				</svg>
			</div>
			<div class="min-w-0 flex-1 text-xs font-medium text-uoft-warm-red">
				{message}
			</div>
		</div>
	</div>
{/if}
