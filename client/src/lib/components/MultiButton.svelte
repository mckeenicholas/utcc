<script lang="ts">
interface Props {
	selectedIndex: number;
	labels: string[];
}

let { selectedIndex = $bindable(), labels }: Props = $props();
</script>

<div class="inline-flex rounded-md border border-gray-200 bg-white">
	{#each labels as label, index (index)}
		<button
			onclick={() => (selectedIndex = index)}
			class="min-h-[40px] border-gray-200 px-4 py-2 text-sm font-medium transition-colors {selectedIndex == index
			? 'bg-blue-600 text-white'
			: 'bg-white transition-colors duration-100 ease-in-out hover:bg-gray-100'}
            {index == 0 && "rounded-l-md border-r"}
             {index == labels.length - 1 && "rounded-r-md border-l"}"
		>
			{label}
		</button>
	{/each}
</div>
