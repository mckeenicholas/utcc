<script lang="ts">
	import { goto } from '$app/navigation';
	import type { Competition } from '$lib/types';

	interface Props {
		competition: Competition;
	}

	let { competition }: Props = $props();
</script>

<div class="overflow-hidden rounded-lg bg-white shadow">
	<div class="px-4 py-5 sm:p-6">
		<div class="flex items-center">
			<div class="flex-shrink-0">
				<div class="flex h-10 w-10 items-center justify-center rounded-md bg-blue-500 text-white">
					<svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							stroke-width="2"
							d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
						/>
					</svg>
				</div>
			</div>
			<div class="ml-5 w-0 flex-1">
				<dl>
					<dt class="truncate text-sm font-medium text-gray-500">
						{competition.name}
					</dt>
					<dd class="flex items-baseline">
						<div class="text-lg font-medium text-gray-900">
							{new Date(competition.date).toLocaleDateString()}
						</div>
					</dd>
				</dl>
			</div>
		</div>
	</div>
	<div class=" px-4 py-4 sm:px-6">
		<div class="text-sm">
			<button
				onclick={() => goto(`/dashboard/competitions/${competition.id}`)}
				class="font-medium text-blue-600 hover:text-blue-500"
			>
				View competition<span class="sr-only"> {competition.name}</span>
			</button>
		</div>
	</div>
</div>
