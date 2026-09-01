<script lang="ts">
import type { Competition } from "$lib/types";
import { formatCompetitionDate } from "$lib/utils";
import CubeIcon from "./CubeIcon.svelte";

interface Props {
	competition: Competition;
}

const { competition }: Props = $props();
</script>

<a href="/competitions/{competition.id}" class="group block">
	<div class="border border-gray-200 bg-white p-4 transition-colors group-hover:border-uoft-blue sm:p-5">
		<div class="flex items-center justify-between gap-4">
			<div class="min-w-0 flex-1">
				<div class="flex items-center gap-2">
					{#if competition.session_name}
						<span class="rounded-sm bg-gray-100 px-2 py-0.5 text-xs font-semibold text-uoft-blue">
							{competition.session_name}
						</span>
					{/if}
					<span class="text-xs text-gray-700">
						{formatCompetitionDate(competition.date)}
					</span>
				</div>
				<h2
					class="mt-1 text-base font-bold tracking-tight text-gray-900 transition-colors group-hover:text-uoft-blue sm:text-lg"
				>
					{competition.name}
				</h2>
				<div class="mt-2.5 flex flex-wrap items-center gap-1.5">
					{#each competition.events as event (event)}
						<CubeIcon {event} class="text-sm text-gray-700 transition-colors group-hover:text-uoft-blue" />
					{/each}
				</div>
			</div>

			<span
				class="inline-flex shrink-0 items-center rounded-sm border border-gray-200 bg-gray-50 px-3 py-1.5 text-xs font-medium text-gray-700 transition-colors group-hover:border-uoft-blue group-hover:bg-uoft-blue group-hover:text-white"
			>
				Results &rarr;
			</span>
		</div>
	</div>
</a>
