<script lang="ts">
interface Props {
	value: boolean;
	leftLabel: string;
	rightLabel: string;
}

let { value = $bindable(), leftLabel, rightLabel }: Props = $props();
</script>

<div class="inline-flex rounded-sm border border-border bg-surface">
	<button
		type="button"
		onclick={() => (value = false)}
		class="h-9 rounded-l-sm border-r border-border px-3.5 text-xs font-semibold transition-colors {!value
			? 'bg-uoft-blue text-white dark:border dark:border-blue-500/30'
			: 'bg-surface text-secondary hover:bg-surface-muted'}"
	>
		{leftLabel}
	</button>
	<button
		type="button"
		onclick={() => (value = true)}
		class="h-9 rounded-r-sm px-3.5 text-xs font-semibold transition-colors {value
			? 'bg-uoft-blue text-white dark:border dark:border-blue-500/30'
			: 'bg-surface text-secondary hover:bg-surface-muted'}"
	>
		{rightLabel}
	</button>
</div>
