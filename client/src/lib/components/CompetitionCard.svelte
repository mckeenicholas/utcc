<script lang="ts">
import type { Competition } from "#lib/types.js";
import { formatCompetitionDate } from "#lib/utils.js";
import CubeIcon from "./CubeIcon.svelte";

interface Props {
	competition: Competition;
}

const { competition }: Props = $props();
</script>

<a href="/competitions/{competition.id}" class="group block">
	<div class="border border-border bg-surface p-4 transition-colors group-hover:border-brand sm:p-5">
		<div class="flex items-center justify-between gap-4">
			<div class="min-w-0 flex-1">
				<div class="flex items-center gap-2">
					{#if competition.session_name}
						<span class="rounded-sm bg-surface-muted px-2 py-0.5 text-xs font-semibold text-brand">
							{competition.session_name}
						</span>
					{/if}
					<span class="text-xs text-secondary">
						{formatCompetitionDate(competition.date)}
					</span>
				</div>
				<h2
					class="mt-1 text-base font-bold tracking-tight text-main transition-colors group-hover:text-brand sm:text-lg"
				>
					{competition.name}
				</h2>
				<div class="mt-2.5 flex flex-wrap items-center gap-1.5">
					{#each competition.events as event (event)}
						<CubeIcon {event} class="text-sm text-secondary transition-colors group-hover:text-brand" />
					{/each}
				</div>
			</div>

			<span
				class="inline-flex shrink-0 items-center rounded-sm border border-border bg-surface-subtle px-3 py-1.5 text-xs font-medium text-secondary transition-colors group-hover:border-brand group-hover:bg-uoft-blue group-hover:text-white"
			>
				Results &rarr;
			</span>
		</div>
	</div>
</a>
