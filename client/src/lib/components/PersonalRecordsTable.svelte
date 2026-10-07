<script lang="ts">
import { type ProfileRecordDetail, type WCAEvent, eventNames } from "#lib/types.js";
import { renderTime } from "#lib/utils.js";

const { records }: { records: [string, ProfileRecordDetail][] } = $props();
</script>

<div class="mb-6 overflow-hidden border border-border bg-surface">
	<div class="border-b border-border bg-surface-subtle px-4 py-2.5 sm:px-5">
		<h2 class="text-sm font-bold tracking-tight text-main">Personal Records</h2>
	</div>
	<div class="overflow-x-auto">
		<table class="min-w-full divide-y divide-border">
			<thead class="bg-surface-subtle">
				<tr>
					<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-secondary uppercase"> Event </th>
					<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-secondary uppercase"> Single </th>
					<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-brand uppercase"> Average </th>
				</tr>
			</thead>
			<tbody class="divide-y divide-border bg-surface">
				{#each records as [eventName, data] (eventName)}
					<tr class="transition-colors hover:bg-surface-muted">
						<td class="px-4 py-2.5 text-sm font-medium whitespace-nowrap text-main">
							<div class="flex items-center gap-2">
								<span class="cubing-icon event-{eventName} text-sm text-brand"></span>
								<span>{eventNames[eventName as WCAEvent]}</span>
							</div>
						</td>
						<td class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-main tabular-nums">
							{renderTime(data.single)}
						</td>
						<td class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-brand tabular-nums">
							{renderTime(data.average)}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
