<script lang="ts">
interface Props {
	value: boolean;
	leftLabel: string;
	rightLabel: string;
}

let { value = $bindable(), leftLabel, rightLabel }: Props = $props();
</script>

<div class="inline-flex rounded-sm border border-gray-200 bg-white">
	<button
		type="button"
		onclick={() => (value = false)}
		class="h-[36px] rounded-l-sm border-r border-gray-200 px-3.5 text-xs font-semibold transition-colors {!value
			? 'bg-uoft-blue text-white'
			: 'bg-white text-gray-700 hover:bg-gray-50'}"
	>
		{leftLabel}
	</button>
	<button
		type="button"
		onclick={() => (value = true)}
		class="h-[36px] rounded-r-sm px-3.5 text-xs font-semibold transition-colors {value
			? 'bg-uoft-blue text-white'
			: 'bg-white text-gray-700 hover:bg-gray-50'}"
	>
		{rightLabel}
	</button>
</div>
