<script lang="ts">
interface Props {
	selectedIndex: number;
	labels: string[];
	vertical?: boolean;
}

let { selectedIndex = $bindable(), labels, vertical = false }: Props = $props();
</script>

<div class="inline-flex rounded-sm border border-gray-200 bg-white {vertical ? 'w-full flex-col' : 'items-center'}">
	{#each labels as label, index (index)}
		<button
			type="button"
			onclick={() => (selectedIndex = index)}
			class="{vertical ? 'w-full px-3 py-2 text-left' : 'h-[36px] px-3.5'} text-xs font-semibold transition-colors
				{selectedIndex === index ? 'bg-uoft-blue text-white' : 'bg-white text-gray-700 hover:bg-gray-50'}
				{!vertical && index > 0 && 'border-l border-gray-200'}
				{!vertical && index === 0 && 'rounded-l-sm'}
				{!vertical && index === labels.length - 1 && 'rounded-r-sm'}
				{vertical && index > 0 && 'border-t border-gray-200'}
				{vertical && index === 0 && 'rounded-t-sm'}
				{vertical && index === labels.length - 1 && 'rounded-b-sm'}"
		>
			{label}
		</button>
	{/each}
</div>
