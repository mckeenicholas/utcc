<script lang="ts">
const { title, showBack = false }: { title: string; showBack?: boolean } = $props();
</script>

<div class="flex flex-col gap-3 border-b border-border pb-5 sm:flex-row sm:items-center sm:justify-between">
	<h1 class="text-2xl font-bold tracking-tight text-main sm:text-3xl">{title}</h1>
	<div class="flex items-center gap-2">
		{#if showBack}
			<a
				href="/dashboard"
				class="rounded-sm border border-border bg-surface px-3 py-1.5 text-xs font-medium text-secondary transition-colors hover:bg-surface-muted focus:outline-none"
			>
				&larr; Dashboard
			</a>
		{/if}

		<a
			href="/dashboard/signout"
			class="rounded-sm border border-red-200 bg-surface px-3 py-1.5 text-xs font-medium text-uoft-warm-red transition-colors hover:bg-red-50 focus:outline-none dark:border-red-900/50 dark:text-red-400 dark:hover:bg-red-950/40"
		>
			Sign Out
		</a>
	</div>
</div>
