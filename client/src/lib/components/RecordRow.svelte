<script lang="ts">
import type { RecordInstance, WCAEvent } from "$lib/types";
import { getMeanType, renderTime } from "$lib/utils";

const {
	record,
	eventKey,
	type,
}: { record: RecordInstance | undefined; eventKey: WCAEvent; type: "Single" | "Average" } = $props();

const recordType = $derived.by(() => {
	if (type === "Single") {
		return "Single";
	}

	return getMeanType(eventKey);
});
</script>

{#if record}
	<tr class="transition-colors hover:bg-gray-50/80">
		<td class="px-4 py-2.5 text-xs font-semibold tracking-wider whitespace-nowrap text-gray-700 uppercase">
			{recordType}
		</td>

		<td class="px-4 py-2.5 text-left text-sm font-medium whitespace-nowrap text-gray-900">
			<a href="/persons/{record.person}" class="transition-colors hover:text-uoft-blue hover:underline">
				{record.person_name}
			</a>
		</td>
		<td class="px-4 py-2.5 text-left text-sm whitespace-nowrap text-gray-600">
			<a class="transition-colors hover:text-uoft-blue hover:underline" href="/competitions/{record.competition_id}">
				{record.competition_name}
			</a>
		</td>
		<td class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-uoft-blue tabular-nums">
			{renderTime(record.result)}
		</td>
		{#each record.times_list as time, timeIdx (timeIdx)}
			<td
				class="hidden px-4 py-2.5 text-right font-mono text-sm whitespace-nowrap text-gray-600 tabular-nums md:table-cell"
			>
				{renderTime(time)}
			</td>
		{/each}
	</tr>
{/if}
