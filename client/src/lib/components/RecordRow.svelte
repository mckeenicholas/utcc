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

<tr
	class="hover: cursor-pointer transition-colors duration-150 ease-in-out"
	onclick={() => (window.location.href = `/competition/${record.competition_id}`)}
>
	<td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
		{recordType}
	</td>
	<td class="whitespace-nowrap px-6 py-4 text-sm font-medium text-gray-900">
		{record.person}
	</td>
	<td class="whitespace-nowrap px-6 py-4 text-sm text-gray-700">
		{record.competition_name}
	</td>
	<td class="whitespace-nowrap px-6 py-4 text-center font-mono text-sm font-bold text-gray-900">
		{renderTime(record.result)}
	</td>
	{#each record.times_list as time, timeIdx (timeIdx)}
		<td
			class="hidden whitespace-nowrap px-6 py-4 text-center font-mono text-sm text-gray-700 md:table-cell"
		>
			{renderTime(time)}
		</td>
	{/each}
</tr>
