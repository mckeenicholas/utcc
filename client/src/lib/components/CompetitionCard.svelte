<script lang="ts">
import type { Competition } from "$lib/types";
import { formatCompetitionDate } from "$lib/utils";
import CubeIcon from "./CubeIcon.svelte";

interface Props {
	competition: Competition;
}

const { competition }: Props = $props();
</script>

<div
	class="overflow-hidden rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition-all duration-200 hover:shadow-md"
>
	<div class="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
		<div class="min-w-0 flex-1">
			<h3 class="truncate text-lg font-bold text-gray-900">
				{competition.name}
			</h3>
			<p class="mt-1 text-sm font-medium text-gray-500">
				{formatCompetitionDate(competition.date)}
			</p>
		</div>
		<div class="flex shrink-0 flex-wrap gap-1.5">
			{#each competition.events as event (event)}
				<CubeIcon {event} class="text-lg text-gray-600 transition-colors hover:text-blue-600" />
			{/each}
		</div>
	</div>
	<div class="mt-4 flex items-center justify-between border-t border-gray-100 pt-4">
		<a
			href="/competitions/{competition.id}"
			class="text-sm font-semibold text-blue-600 transition-colors hover:text-blue-500"
		>
			View Results
			<span class="sr-only"> for {competition.name}</span>
		</a>
		<svg
			class="h-4 w-4 text-gray-400 transition-transform group-hover:translate-x-1"
			fill="none"
			stroke="currentColor"
			viewBox="0 0 24 24"
		>
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
		</svg>
	</div>
</div>
