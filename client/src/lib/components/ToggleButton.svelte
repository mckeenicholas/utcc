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
		class="min-h-[40px] rounded-l-md border-r border-gray-200 px-4 py-2 text-sm font-medium transition-colors {!value
			? 'bg-blue-600 text-white'
			: 'bg-white transition-colors duration-100 ease-in-out hover:bg-gray-100'}"
	>
		{leftLabel}
	</button>
	<button
		onclick={() => (value = true)}
		class="min-h-[40px] rounded-r-md px-4 py-2 text-sm font-medium transition-colors {value
			? 'bg-blue-600 text-white'
			: 'bg-white transition-colors duration-100 ease-in-out hover:bg-gray-100'}"
	>
		{rightLabel}
	</button>
</div>
