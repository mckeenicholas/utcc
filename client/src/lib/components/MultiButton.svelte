<script lang="ts">
interface Props {
	selectedIndex: number;
	labels: string[];
	vertical?: boolean;
}

const { selectedIndex = $bindable(), labels, vertical = false }: Props = $props();
</script>

<div class="flex rounded-md border border-gray-200 bg-white {vertical && 'w-full flex-col'}">
	{#each labels as label, index (index)}
		<button
			onclick={() => (selectedIndex = index)}
			class="min-h-[40px] border-gray-200 px-4 py-2 text-sm font-medium transition-colors
				{selectedIndex == index
				? 'bg-blue-600 text-white'
				: 'bg-white transition-colors duration-100 ease-in-out hover:bg-gray-100'}
				{!vertical && index == 0 && 'rounded-l-md border-r'}
				{!vertical && index == labels.length - 1 && 'rounded-r-md border-l'}
				{vertical && index == 0 && 'rounded-t-md border-b'}
				{vertical && index == labels.length - 1 && 'rounded-b-md border-t'}"
		>
			{label}
		</button>
	{/each}
</div>
