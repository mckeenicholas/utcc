<script lang="ts">
import type { ClassValue } from "svelte/elements";
import { Tooltip } from "bits-ui";
import { type WCAEvent, eventNames } from "$lib/types";

const { event, class: className }: { event: WCAEvent; class?: ClassValue } = $props();
</script>

<Tooltip.Provider>
	<Tooltip.Root delayDuration={200}>
		<Tooltip.Trigger>
			{#snippet child({ props })}
				<span {...props} class="cubing-icon event-{event} {className}" aria-label={eventNames[event]}></span>
			{/snippet}
		</Tooltip.Trigger>
		<Tooltip.Content>
			<div class="rounded-sm border border-gray-200 bg-white px-2 py-0.5 text-xs text-gray-700">
				{eventNames[event]}
			</div>
		</Tooltip.Content>
	</Tooltip.Root>
</Tooltip.Provider>
