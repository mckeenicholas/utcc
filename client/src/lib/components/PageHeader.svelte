<script lang="ts">
import { goto } from '$app/navigation';
import type { Competition } from '$lib/types';

interface Props {
	competition: Competition | null;
	backUrl?: string;
	backText?: string;
}

let { competition, backUrl = '/dashboard', backText = 'Back to Dashboard' }: Props = $props();
</script>

<div class="mb-8 flex items-center justify-between">
	<div class="flex items-center space-x-4">
		<button
			onclick={() => goto(backUrl)}
			class="inline-flex items-center rounded-md bg-gray-100 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-200 focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 focus:outline-none"
		>
			<svg class="mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
			</svg>
			{backText}
		</button>
		{#if competition}
			<div>
				<h1 class="text-3xl font-bold text-gray-900">{competition.name}</h1>
				<p class="text-gray-600">Date: {new Date(competition.date).toLocaleDateString()}</p>
			</div>
		{/if}
	</div>
</div>
