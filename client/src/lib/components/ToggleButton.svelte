<script lang="ts">
	interface Props {
		value: boolean;
		leftLabel: string;
		rightLabel: string;
	}

	let { value = $bindable(), leftLabel, rightLabel }: Props = $props();
</script>

<div class="inline-flex rounded-md border border-gray-200 bg-white">
	<button
		onclick={() => (value = false)}
		class="rounded-l-md border-r border-gray-200 px-4 py-2 text-sm font-medium transition-colors {!value
			? 'bg-blue-600 text-white'
			: 'bg-white text-gray-700 hover:bg-gray-50'}"
	>
		{leftLabel}
	</button>
	<button
		onclick={() => (value = true)}
		class="rounded-r-md px-4 py-2 text-sm font-medium transition-colors {value
			? 'bg-blue-600 text-white'
			: 'bg-white text-gray-700 hover:bg-gray-50'}"
	>
		{rightLabel}
	</button>
</div>
