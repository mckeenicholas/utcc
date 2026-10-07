<script lang="ts">
import type { ClassValue } from "svelte/elements";
import { Tooltip } from "bits-ui";
import { type WCAEvent, eventNames } from "#lib/types.js";

const { event, class: className }: { event: WCAEvent; class?: ClassValue } = $props();

const iconClass = $derived(event === "fto" ? "unofficial-fto" : `event-${event}`);
</script>

<Tooltip.Provider>
	<Tooltip.Root delayDuration={200}>
		<Tooltip.Trigger>
			{#snippet child({ props })}
				<span {...props} class="cubing-icon {iconClass} {className}" aria-label={eventNames[event]}></span>
			{/snippet}
		</Tooltip.Trigger>
		<Tooltip.Content>
			<div class="z-50 rounded-sm border border-border bg-surface px-2 py-0.5 text-xs text-main shadow-xs">
				{eventNames[event]}
			</div>
		</Tooltip.Content>
	</Tooltip.Root>
</Tooltip.Provider>
