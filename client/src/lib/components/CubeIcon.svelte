<script lang="ts">
import type { ClassValue } from "svelte/elements";
import { eventNames, type WCAEvent } from "$lib/types";
import "../icons.css";
import { Tooltip } from "bits-ui";

const { event, class: className }: { event: WCAEvent; class?: ClassValue } = $props();
</script>

<Tooltip.Provider>
	<Tooltip.Root delayDuration={200}>
		<Tooltip.Trigger class={className}>
			<div class="icon cubing-icon event-{event}"></div>
		</Tooltip.Trigger>
		<Tooltip.Content>
			<div class="rounded-md border border-gray-300 bg-white px-2 ease-in-out">
				{eventNames[event]}
			</div>
		</Tooltip.Content>
	</Tooltip.Root>
</Tooltip.Provider>
