<script lang="ts">
import { type ProfileRecordDetail, type WCAEvent, eventNames } from "$lib/types";
import { renderTime } from "$lib/utils";

const { records }: { records: [string, ProfileRecordDetail][] } = $props();
</script>

<div class="mb-6 overflow-hidden border border-gray-200 bg-white">
	<div class="border-b border-gray-200 bg-gray-50 px-4 py-2.5 sm:px-5">
		<h2 class="text-sm font-bold tracking-tight text-gray-900">Personal Records</h2>
	</div>
	<div class="overflow-x-auto">
		<table class="min-w-full divide-y divide-gray-200">
			<thead class="bg-gray-50">
				<tr>
					<th class="px-4 py-2.5 text-left text-xs font-semibold tracking-wider text-gray-700 uppercase"> Event </th>
					<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-gray-700 uppercase"> Single </th>
					<th class="px-4 py-2.5 text-right text-xs font-semibold tracking-wider text-uoft-blue uppercase">
						Average
					</th>
				</tr>
			</thead>
			<tbody class="divide-y divide-gray-100 bg-white">
				{#each records as [eventName, data] (eventName)}
					<tr class="transition-colors hover:bg-gray-50/80">
						<td class="px-4 py-2.5 text-sm font-medium whitespace-nowrap text-gray-900">
							<div class="flex items-center gap-2">
								<span class="cubing-icon event-{eventName} text-sm text-uoft-blue"></span>
								<span>{eventNames[eventName as WCAEvent]}</span>
							</div>
						</td>
						<td class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-gray-900 tabular-nums">
							{renderTime(data.single)}
						</td>
						<td
							class="px-4 py-2.5 text-right font-mono text-sm font-bold whitespace-nowrap text-uoft-blue tabular-nums"
						>
							{renderTime(data.average)}
						</td>
					</tr>
				{/each}
			</tbody>
		</table>
	</div>
</div>
