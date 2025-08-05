<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Competition } from '$lib/types';
	import CubeIcon from './CubeIcon.svelte';

	interface Props {
		competition: Competition;
	}

	let { competition }: Props = $props();
</script>

<div class="overflow-hidden rounded-lg bg-white ps-6 shadow">
	<div class="flex flex-row items-start py-3">
		<div class="flex items-center">
			<div class="flex-1">
				<dl>
					<dt class="text-lg font-semibold text-gray-900">
						{competition.name}
					</dt>
					<dd class="flex items-baseline">
						<div class="truncate text-sm font-medium text-gray-500">
							{new Date(competition.date).toLocaleDateString()}
						</div>
					</dd>
				</dl>
			</div>
		</div>
		<div class="ms-6 flex flex-wrap gap-2">
			{#each competition.events as event (event)}
				<CubeIcon {event} class="text-lg text-gray-700" />
			{/each}
		</div>
	</div>
	<div class="pb-4">
		<div class="text-sm">
			<button
				onclick={() => goto(`/competitions/${competition.id}`)}
				class="font-medium text-blue-600 hover:text-blue-500"
			>
				View results<span class="sr-only"> {competition.name}</span>
			</button>
		</div>
	</div>
</div>
