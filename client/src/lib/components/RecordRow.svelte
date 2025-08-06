<script lang="ts">
import { getMeanType, renderTime } from '$lib/utils';
import type { RecordInstance, WCAEvent } from '$lib/types';

let {
	record,
	eventKey,
	type
}: { record: RecordInstance; eventKey: WCAEvent; type: 'Single' | 'Average' } = $props();

let recordType = $derived.by(() => {
	if (type == 'Single') {
		return 'Single';
	}

	return getMeanType(eventKey);
});
</script>

<tr class="transition-colors duration-100 ease-in-out hover:bg-gray-100">
	<td class="px-6 py-4 text-sm font-medium whitespace-nowrap text-gray-900">
		{recordType}
	</td>
	<td class="px-6 py-4 text-sm font-medium whitespace-nowrap text-gray-900">
		{record.person_name}
	</td>
	<td class="px-6 py-4 text-sm whitespace-nowrap text-gray-700">
		<a class="hover:text-gray-400" href={`/competitions/${record.competition_id}`}>
			{record.competition_name}</a
		>
	</td>
	<td class="px-6 py-4 text-center font-mono text-sm font-bold whitespace-nowrap text-gray-900">
		{renderTime(record.result)}
	</td>
	{#each record.times_list as time, timeIdx (timeIdx)}
		<td
			class="hidden px-6 py-4 text-center font-mono text-sm whitespace-nowrap text-gray-700 md:table-cell"
		>
			{renderTime(time)}
		</td>
	{/each}
</tr>
